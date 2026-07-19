from app.repositories.sector_repository import SectorRepository

class SectorService:
    def __init__(self, repository: SectorRepository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.find_all()

    async def get_by_id(self, sector_id: int):
        return await self.repository.find_by_id(sector_id)

    async def get_by_segment_number(self, segment_number: int):
        return await self.repository.find_by_segment_number(segment_number)