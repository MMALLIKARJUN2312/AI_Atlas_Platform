from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import CandidateResponse, CompanyWrite, DiscoveryRequest
from app.admin.service import AdminService
from app.api.deps import get_current_admin_user, get_database
from app.api.deps_ai import get_indexing_service, get_llm_service
from app.rag.vector_store.indexing_service import IndexingService
from app.ai.services.llm_service import LLMService

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])
Database = Annotated[AsyncSession, Depends(get_database)]


def get_admin_service(db: Database, llm: LLMService = Depends(get_llm_service), indexing: IndexingService = Depends(get_indexing_service)) -> AdminService:
    return AdminService(db, llm, indexing)


Service = Annotated[AdminService, Depends(get_admin_service)]


@router.post("/discover", response_model=list[CandidateResponse])
async def discover(request: DiscoveryRequest, service: Service): return await service.discover(request)


@router.get("/candidates", response_model=list[CandidateResponse])
async def candidates(service: Service): return await service.list_candidates()


@router.post("/candidates/{candidate_id}/approve")
async def approve(candidate_id: int, service: Service): return await service.approve(candidate_id)


@router.post("/candidates/{candidate_id}/reject", response_model=CandidateResponse)
async def reject(candidate_id: int, service: Service): return await service.reject(candidate_id)


@router.post("/companies")
async def create_company(data: CompanyWrite, service: Service): return await service.create_company(data)


@router.put("/companies/{company_id}")
async def update_company(company_id: int, data: CompanyWrite, service: Service): return await service.update_company(company_id, data)
