from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.ask_ai import router as ask_ai_router
from app.api.routes.companies import router as company_router
from app.api.routes.sectors import router as sector_router
from app.api.routes.problems import router as problem_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(ask_ai_router)
api_router.include_router(company_router, prefix="/companies", tags=["Companies"])
api_router.include_router(sector_router)
api_router.include_router(problem_router)