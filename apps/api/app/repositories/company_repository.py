from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select

from app.database.models.company import Company
from app.repositories.base_repository import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, Company) 
        
    async def find_all(
        self,
        *,
        search: str | None = None,
        segment: str | None = None,
        company_type: str | None = None,
        maturity: str | None = None,
        ai_category: str | None = None,
    ) -> list[Company]:
        statement = select(Company)

        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Company.vendor_name.ilike(pattern),
                    Company.ai_category.ilike(pattern),
                    Company.food_beverage_ai_use_case.ilike(pattern),
                )
            )

        if segment:
            statement = statement.where(Company.segment_tags.ilike(f"%{segment.strip()}%"))

        if company_type:
            statement = statement.where(Company.company_type == company_type.strip())

        if maturity:
            statement = statement.where(Company.maturity == maturity.strip())

        if ai_category:
            statement = statement.where(Company.ai_category.ilike(f"%{ai_category.strip()}%"))

        result = await self.db.scalars(statement.order_by(Company.vendor_name))
        return list(result)
    
    async def bulk_insert_dataset(self, companies : list[Company]) -> int:
        return await self.bulk_insert_ignore_conflicts(companies, ["vendor_name"])
    
    async def find_by_vendor_name(self, vendor_name : str) -> Company | None:
        return await self.db.scalar(select(Company).where(Company.vendor_name == vendor_name))
    
    async def find_by_id(self, company_id: int) -> Company | None:
        return await self.db.scalar(select(Company).where(Company.id == company_id))

    async def search(self, query: str) -> list[Company]:
        return await self.find_all(search=query)
