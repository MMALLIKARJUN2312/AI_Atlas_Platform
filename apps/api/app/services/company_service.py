from app.repositories.company_repository import CompanyRepository

class CompanyService:

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    async def list_companies(
        self,
        *,
        search: str | None = None,
        segment: str | None = None,
        company_type: str | None = None,
        maturity: str | None = None,
        ai_category: str | None = None,
    ):
        return await self.repository.find_all(
            search=search,
            segment=segment,
            company_type=company_type,
            maturity=maturity,
            ai_category=ai_category,
        )

    async def get_all(self):
        return await self.list_companies()

    async def get(self, company_id: int):
        return await self.repository.find_by_id(company_id)

    async def search(self, query: str):
        return await self.list_companies(search=query)
