from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models.sector import Sector
from app.repositories.base_repository import BaseRepository

class SectorRepository(BaseRepository[Sector]):
    def __init__(self, db : AsyncSession):
        super().__init__(db, Sector)
        
    async def find_all(self) -> list[Sector]:
        result = await self.db.scalars(select(Sector))
        return list(result)
     
    async def bulk_insert_dataset(self, sectors : list[Sector]) -> int:
        return await self.bulk_insert_ignore_conflicts(sectors, ["segment_name"])    
        
    async def find_by_segment_number(self, segment_number : int) -> Sector | None:
        await self.db.scalar(select(Sector).where(Sector.segment_number == segment_number))