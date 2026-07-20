from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_database
from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
Database = Annotated[AsyncSession, Depends(get_database)]


def get_auth_service(db: Database) -> AuthService:
    return AuthService(db)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, service: Annotated[AuthService, Depends(get_auth_service)]):
    return await service.login(request)
