from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models.company import Company
from app.repositories.base_repository import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, Company) 
        
    async def find_all(self) -> list[Company]:
        result = await self.db.scalars(select(Company))
        return list(result)
    
    async def bulk_insert_dataset(self, companies : list[Company]) -> int:
        return await self.bulk_insert_ignore_conflicts(companies, ["vendor_name"])
    
    async def find_by_vendor_name(self, vendor_name : str) -> Company | None:
        return await self.db.scalar(select(Company).where(Company.vendor_name == vendor_name))
    
    async def find_by_id(self, company_id: int) -> Company | None:
        return await self.db.scalar(select(Company).where(Company.id == company_id))

    async def search(self, query: str) -> list[Company]:

        statement = (select(Company).where(Company.vendor_name.ilike(f"%{query}%")).order_by(Company.vendor_name))

        result = await self.db.scalars(statement)

        return list(result)