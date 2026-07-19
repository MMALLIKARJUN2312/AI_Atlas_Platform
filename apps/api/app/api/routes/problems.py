from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.problem_response import ProblemResponse
from app.database.session import get_db
from app.repositories.company_repository import CompanyRepository
from app.repositories.problem_company_mapping_repository import (
    ProblemCompanyMappingRepository,
)
from app.repositories.problem_repository import ProblemRepository
from app.services.problem_service import ProblemService

router = APIRouter(tags=["Problems"])

def get_problem_service(
    db: AsyncSession = Depends(get_db),
) -> ProblemService:
    return ProblemService(
        CompanyRepository(db),
        ProblemCompanyMappingRepository(db),
        ProblemRepository(db),
    )


@router.get(
    "/companies/{company_id}/problems",
    response_model=list[ProblemResponse],
)
async def get_company_problems(
    company_id: int,
    service: ProblemService = Depends(get_problem_service),
):
    return await service.get_company_problems(company_id)