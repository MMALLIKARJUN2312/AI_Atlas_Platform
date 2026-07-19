from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sector_response import SectorResponse
from app.database.session import get_db
from app.repositories.sector_repository import SectorRepository
from app.services.sector_service import SectorService

router = APIRouter(prefix="/sectors", tags=["Sectors"])

def get_sector_service(
    db: AsyncSession = Depends(get_db),
) -> SectorService:
    repository = SectorRepository(db)
    return SectorService(repository)


@router.get("", response_model=list[SectorResponse])
async def get_sectors(
    service: SectorService = Depends(get_sector_service),
):
    return await service.get_all()


@router.get("/{sector_id}", response_model=SectorResponse)
async def get_sector(
    sector_id: int,
    service: SectorService = Depends(get_sector_service),
):
    sector = await service.get_by_id(sector_id)

    if sector is None:
        raise HTTPException(
            status_code=404,
            detail="Sector not found",
        )

    return sector