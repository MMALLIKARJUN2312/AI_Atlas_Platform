from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.problem_company_mapping import ProblemCompanyMapping
from app.repositories.base_repository import BaseRepository

class ProblemCompanyMappingRepository(BaseRepository[ProblemCompanyMapping]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, ProblemCompanyMapping)
        
    async def find_all(self) -> list[ProblemCompanyMapping]:
        result = await self.db.scalars(select(ProblemCompanyMapping))
        return list(result)
        
    async def bulk_insert_dataset(self, mappings : list[ProblemCompanyMapping]) -> int:
        return await self.bulk_insert_ignore_conflicts(mappings, ["problem_statement"])