from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.problem_company_mapping import ProblemCompanyMapping
from app.repositories.base_repository import BaseRepository

class ProblemCompanyMappingRepository(BaseRepository[ProblemCompanyMapping]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, ProblemCompanyMapping)
        
    async def bulk_insert_dataset(self, mappings : list[ProblemCompanyMapping]) -> int:
        return await self.bulk_insert_ignore_conflicts(mappings, ["problem_statement"])