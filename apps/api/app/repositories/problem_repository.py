from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models.problem import Problem
from app.repositories.base_repository import BaseRepository

class ProblemRepository(BaseRepository[Problem]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, Problem)
        
    async def find_all(self) -> list[Problem]:
        result = await self.db.scalars(select(Problem))
        return list(result)
        
    async def bulk_insert_dataset(self, problems : list[Problem]) -> int:
        return await self.bulk_insert_ignore_conflicts(problems, ["problem_id"])
        
    async def find_by_problem_id(self, problem_id : str) -> Problem | None:
        return await self.db.scalar(select(Problem).where(Problem.problem_id == problem_id))
    
    async def find_by_problem_statement(self, problem_statement: str) -> Problem | None:
        return await self.db.scalar(select(Problem).where(Problem.problem_statement == problem_statement))