from datetime import datetime, timezone

import pytest

from app.database.models.company import Company
from app.services.news_service import NewsCandidate, NewsService


class FakeCompanyRepository:
    def __init__(self, company: Company):
        self.company = company

    async def find_by_id(self, company_id: int) -> Company | None:
        return self.company if company_id == self.company.id else None


class FakeNewsRepository:
    def __init__(self):
        self.urls: set[str] = set()

    async def exists_by_url(self, url: str) -> bool:
        return url in self.urls

    async def bulk_create_news(self, news_items):
        for index, item in enumerate(news_items, start=1):
            item.id = index
            item.created_at = datetime.now(timezone.utc)
            item.updated_at = item.created_at
            self.urls.add(item.source_url)
        return news_items


@pytest.mark.asyncio
async def test_refresh_company_news_filters_existing_urls():
    company = Company(id=7, vendor_name="Example Foods GmbH", country="Germany")
    repository = FakeNewsRepository()
    service = NewsService(repository, FakeCompanyRepository(company))

    async def fetch_news(_: Company):
        return [
            NewsCandidate(
                title="Example Foods launches AI quality programme",
                summary="The German food company expanded its AI programme.",
                source_name="Example News",
                source_url="https://example.com/article",
                published_at=datetime.now(timezone.utc),
                relevance_score=0.9,
            )
        ]

    service.fetch_company_news = fetch_news
    assert len(await service.refresh_company_news(company.id)) == 1
    assert await service.refresh_company_news(company.id) == []


def test_relevance_score_rejects_name_collisions():
    company = Company(id=7, vendor_name="Example Foods GmbH", country="Germany")

    assert NewsService._relevance_score(company, "Example Foods announces expansion", "Germany food AI") >= 0.7
    assert NewsService._relevance_score(company, "Example brand announces expansion", "Germany food AI") == 0
