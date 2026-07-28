from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import ToolParameter, ToolSpec
from app.database.models.company import Company

MAX_LIMIT = 50


class CompanyDirectoryTool(BaseTool):
    """
    Structured, filterable lookup straight against the relational table.

    Vector search is the wrong instrument for counting and exhaustive listing:
    top-k similarity returns *the most similar k*, never "all 23 of them", so
    asking a pure-RAG chatbot "how many Germany-based vendors are in the
    directory" gets you a confident number derived from 10 chunks. This tool
    exists so the agent can answer those questions with SQL, which is exact,
    while keeping semantic search for meaning-based questions.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="query_company_directory",
            description=(
                "Query the structured company directory with exact filters and get exact counts. "
                "Use this - NOT semantic search - whenever the question involves counting "
                "('how many'), complete listings ('list all'), or filtering by an exact "
                "attribute such as country, AI category, market segment, or maturity. "
                "Returns the total match count plus the matching companies."
            ),
            parameters=[
                ToolParameter(name="country", description="Filter by country, e.g. 'Germany'."),
                ToolParameter(
                    name="category",
                    description="Filter by AI category or use case keyword, e.g. 'computer vision', 'forecasting'.",
                ),
                ToolParameter(
                    name="segment",
                    description="Filter by Food & Beverage market segment keyword, e.g. 'brewing', 'dairy', 'bakery'.",
                ),
                ToolParameter(name="maturity", description="Filter by maturity, e.g. 'Growth', 'Enterprise'."),
                ToolParameter(
                    name="limit",
                    description="Maximum companies to return (default 15, max 50).",
                    type="integer",
                ),
            ],
        )

    async def run(
        self,
        country: str = "",
        category: str = "",
        segment: str = "",
        maturity: str = "",
        limit: int = 15,
        **_: object,
    ) -> ToolResult:
        filters = []
        applied: dict[str, str] = {}

        if country.strip():
            filters.append(Company.country.ilike(f"%{country.strip()}%"))
            applied["country"] = country.strip()
        if category.strip():
            filters.append(
                or_(
                    Company.ai_category.ilike(f"%{category.strip()}%"),
                    Company.food_beverage_ai_use_case.ilike(f"%{category.strip()}%"),
                )
            )
            applied["category"] = category.strip()
        if segment.strip():
            filters.append(
                or_(
                    Company.segment_tags.ilike(f"%{segment.strip()}%"),
                    Company.food_beverage_ai_use_case.ilike(f"%{segment.strip()}%"),
                )
            )
            applied["segment"] = segment.strip()
        if maturity.strip():
            filters.append(Company.maturity.ilike(f"%{maturity.strip()}%"))
            applied["maturity"] = maturity.strip()

        limit = max(1, min(int(limit or 15), MAX_LIMIT))

        total = await self.db.scalar(select(func.count(Company.id)).where(*filters)) or 0
        companies = list(
            await self.db.scalars(
                select(Company).where(*filters).order_by(Company.vendor_name).limit(limit)
            )
        )

        if not companies:
            return ToolResult(
                observation=(
                    f"The directory contains 0 companies matching {applied or 'no filters'}. "
                    "Say so plainly rather than guessing."
                ),
                metadata={"total": 0, "filters": applied},
                grounded=True,
            )

        lines = [
            f"Directory query {applied or '(no filters)'} matched {total} companies. "
            f"Showing {len(companies)}:"
        ]
        for company in companies:
            lines.append(
                f"- {company.vendor_name} ({company.country}) | category: {company.ai_category} "
                f"| segments: {company.segment_tags} | maturity: {company.maturity} "
                f"| use case: {company.food_beverage_ai_use_case} | website: {company.website}"
            )

        return ToolResult(
            observation="\n".join(lines),
            sources=[
                Source(
                    title=company.vendor_name,
                    source_type="company",
                    company_id=company.id,
                    url=self._url(company.website),
                    chunk_id=f"directory:company:{company.id}",
                )
                for company in companies
            ],
            metadata={"total": total, "returned": len(companies), "filters": applied},
            grounded=True,
        )

    @staticmethod
    def _url(website: str) -> str | None:
        website = (website or "").strip()
        if not website:
            return None
        return website if website.startswith(("http://", "https://")) else f"https://{website}"
