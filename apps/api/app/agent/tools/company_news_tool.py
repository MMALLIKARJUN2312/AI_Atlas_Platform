from __future__ import annotations

from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import ToolParameter, ToolSpec
from app.database.models.company import Company
from app.database.models.news import News

MAX_LIMIT = 25


class CompanyNewsTool(BaseTool):
    """
    Company-attributed news lookup.

    News is already monitored, relevance-scored and linked to a company row by
    the monitoring pipeline, so this tool reads the *attribution* rather than
    re-deriving it: the agent asks for a company by name and gets that
    company's articles, newest first, each with its real source URL. Semantic
    search can also surface news chunks, but only this path can answer "what is
    the latest news about X" in correct chronological order.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="get_company_news",
            description=(
                "Get recent monitored news articles for a specific company in the directory, "
                "newest first. Use this for any question about news, announcements, funding, "
                "launches, partnerships, or 'what's the latest' regarding a named company. "
                "Omit company_name to get the latest news across all monitored companies."
            ),
            parameters=[
                ToolParameter(
                    name="company_name",
                    description="Name of the company to fetch news for. Partial names are matched.",
                ),
                ToolParameter(
                    name="limit",
                    description="Maximum articles to return (default 8, max 25).",
                    type="integer",
                ),
            ],
        )

    async def run(self, company_name: str = "", limit: int = 8, **_: object) -> ToolResult:
        limit = max(1, min(int(limit or 8), MAX_LIMIT))
        company_name = (company_name or "").strip()

        statement = select(News, Company).join(Company, News.company_id == Company.id)

        if company_name:
            company = await self.db.scalar(
                select(Company).where(
                    or_(
                        Company.vendor_name.ilike(company_name),
                        Company.vendor_name.ilike(f"%{company_name}%"),
                    )
                # Shortest match wins, so "SAP" resolves to SAP rather than "SAP Ariba Logistics".
                ).order_by(func.length(Company.vendor_name))
            )
            if company is None:
                return ToolResult(
                    observation=(
                        f"'{company_name}' is not a company in the AI Atlas directory, so there is "
                        "no monitored news for it. Do not invent news for unknown companies."
                    ),
                    metadata={"articles": 0, "company": company_name},
                    grounded=True,
                )
            statement = statement.where(News.company_id == company.id)

        rows = list(await self.db.execute(statement.order_by(desc(News.published_at)).limit(limit)))

        if not rows:
            scope = f"for {company_name}" if company_name else "across the directory"
            return ToolResult(
                observation=(
                    f"No monitored news articles are stored {scope} yet. State that no news has "
                    "been captured rather than describing news you have not seen."
                ),
                metadata={"articles": 0, "company": company_name},
                grounded=True,
            )

        lines = [f"{len(rows)} monitored news article(s), newest first:"]
        sources: list[Source] = []
        for article, company in rows:
            lines.append(
                f"- [{article.published_at.date().isoformat()}] {company.vendor_name}: "
                f"{article.title} | {article.summary} "
                f"(source: {article.source_name}, relevance {article.relevance_score:.2f}, {article.source_url})"
            )
            sources.append(
                Source(
                    title=article.title,
                    source_type="news",
                    company_id=company.id,
                    url=article.source_url,
                    chunk_id=f"news:{article.id}",
                )
            )

        return ToolResult(
            observation="\n".join(lines),
            sources=sources,
            metadata={"articles": len(rows), "company": company_name},
            grounded=True,
        )
