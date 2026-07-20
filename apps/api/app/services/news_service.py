from __future__ import annotations

import html
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx

from app.database.models.news import News
from app.database.models.company import Company
from app.rag.builders.news_builder import NewsDocumentBuilder
from app.rag.vector_store.indexing_service import IndexingService
from app.repositories.company_repository import CompanyRepository
from app.repositories.news_repository import NewsRepository

logger = logging.getLogger(__name__)

GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search?q={query}&hl=en&gl=DE&ceid=DE:en"
CORPORATE_SUFFIXES = re.compile(r"\b(inc|incorporated|ltd|llc|gmbh|ag|se|co|corp|corporation|group)\b", re.I)
HTML_TAGS = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class NewsCandidate:
    title: str
    summary: str
    source_name: str
    source_url: str
    published_at: datetime
    relevance_score: float


class NewsService:
    def __init__(
        self,
        news_repository: NewsRepository,
        company_repository: CompanyRepository,
        indexing_service: IndexingService | None = None,
    ):
        self.news_repository = news_repository
        self.company_repository = company_repository
        self.indexing_service = indexing_service
        self.news_builder = NewsDocumentBuilder()

    async def get_company_news(self, company_id: int) -> list[News]:
        return await self.news_repository.get_company_news(company_id)

    async def refresh_company_news(self, company_id: int) -> list[News]:
        company = await self.company_repository.find_by_id(company_id)
        if company is None:
            raise LookupError("Company not found")

        candidates = await self.fetch_company_news(company)
        new_articles: list[News] = []
        seen_urls: set[str] = set()

        for candidate in candidates:
            if candidate.source_url in seen_urls or await self.news_repository.exists_by_url(candidate.source_url):
                continue
            seen_urls.add(candidate.source_url)
            new_articles.append(
                News(
                    company_id=company.id,
                    title=candidate.title,
                    summary=candidate.summary,
                    source_name=candidate.source_name,
                    source_url=candidate.source_url,
                    published_at=candidate.published_at,
                    relevance_score=candidate.relevance_score,
                )
            )

        stored_articles = await self.news_repository.bulk_create_news(new_articles)
        await self._index_articles(stored_articles)
        return stored_articles

    async def fetch_company_news(self, company: Company) -> list[NewsCandidate]:
        query = quote_plus(f'"{company.vendor_name}"')
        url = GOOGLE_NEWS_RSS_URL.format(query=query)
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                response = await client.get(url, headers={"User-Agent": "AI-Atlas-NewsBot/1.0"})
                response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Unable to fetch Google News RSS for company_id=%s", company.id)
            return []

        candidates: list[NewsCandidate] = []
        for item in self._parse_rss(response.text):
            score = self._relevance_score(company, item.title, item.summary)
            if score < 0.7:
                continue
            candidates.append(
                NewsCandidate(
                    title=item.title,
                    summary=item.summary,
                    source_name=item.source_name,
                    source_url=item.source_url,
                    published_at=item.published_at,
                    relevance_score=score,
                )
            )
        return candidates

    async def _index_articles(self, articles: list[News]) -> None:
        if self.indexing_service is None:
            logger.warning("News indexing is not configured; %s articles remain pending", len(articles))
            return
        for article in articles:
            try:
                await self.indexing_service.index_document(self.news_builder.build(article))
            except Exception:
                logger.exception("Failed to index news article_id=%s", article.id)

    @staticmethod
    def _parse_rss(payload: str) -> list[NewsCandidate]:
        try:
            root = ElementTree.fromstring(payload)
        except ElementTree.ParseError:
            logger.warning("Google News returned invalid RSS")
            return []

        articles: list[NewsCandidate] = []
        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").strip()
            url = (item.findtext("link") or "").strip()
            if not title or not url:
                continue
            published_raw = item.findtext("pubDate") or ""
            try:
                published_at = parsedate_to_datetime(published_raw).astimezone(timezone.utc)
            except (AttributeError, TypeError, ValueError):
                continue
            source = item.find("source")
            summary = HTML_TAGS.sub("", html.unescape(item.findtext("description") or "")).strip()
            articles.append(
                NewsCandidate(
                    title=title,
                    summary=summary,
                    source_name=(source.text if source is not None and source.text else "Google News").strip(),
                    source_url=url,
                    published_at=published_at,
                    relevance_score=0,
                )
            )
        return articles

    @staticmethod
    def _relevance_score(company: Company, title: str, summary: str) -> float:
        raw_name = re.sub(r"\s+", " ", company.vendor_name.lower()).strip()
        company_name = CORPORATE_SUFFIXES.sub("", company.vendor_name).strip()
        normalized_name = re.sub(r"\s+", " ", company_name.lower())
        article_text = f"{title} {summary}".lower()
        name_matches = raw_name in article_text or (
            len(normalized_name) >= 4 and normalized_name in article_text
        )
        if not name_matches:
            return 0.0
        score = 0.7
        if company.country.lower() in article_text or "germany" in article_text:
            score += 0.1
        if any(term in article_text for term in ("food", "beverage", "ai", "automation", "manufacturing")):
            score += 0.1
        return min(score, 1.0)
