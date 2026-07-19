from app.repositories.company_repository import CompanyRepository

class CompanyService:

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.find_all()

    async def get(self, company_id: int):
        return await self.repository.find_by_id(company_id)

    async def search(self, query: str):
        return await self.repository.search(query)