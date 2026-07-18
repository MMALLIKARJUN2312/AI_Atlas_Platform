from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models.company import Company
from app.repositories.base_repository import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, Company) 
    
    async def bulk_insert_dataset(self, companies : list[Company]) -> int:
        return await self.bulk_insert_ignore_conflicts(companies, ["vendor_name"])
    
    async def find_by_vendor_name(self, vendor_name : str) -> Company | None:
        return await self.db.scalar(select(Company).where(Company.vendor_name == vendor_name))