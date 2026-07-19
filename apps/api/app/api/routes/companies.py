from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_database
from app.schemas.company_response import (CompanyDetailResponse, CompanySummaryResponse)
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService

router = APIRouter()

Database = Annotated[AsyncSession, Depends(get_database)]

def get_company_service(db: Database) -> CompanyService:
    repository = CompanyRepository(db)
    return CompanyService(repository)

Service = Annotated[CompanyService, Depends(get_company_service)]


@router.get(
    "",
    response_model=list[CompanySummaryResponse],
)
async def get_companies(
    service: Service,
    search: str | None = Query(default=None),
):

    if search:
        companies = await service.search(search)
    else:
        companies = await service.get_all()

    return companies


@router.get(
    "/{company_id}",
    response_model=CompanyDetailResponse,
)
async def get_company(
    company_id: int,
    service: Service,
):

    company = await service.get(company_id)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company