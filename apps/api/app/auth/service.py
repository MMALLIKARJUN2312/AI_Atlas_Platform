from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import LoginRequest, TokenResponse
from app.core.security import create_access_token, verify_password
from app.database.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, request: LoginRequest) -> TokenResponse:
        user = await self.db.scalar(select(User).where(User.email == request.email.lower()))
        if not user or not user.is_active or not verify_password(request.password, user.hashed_password):
            raise HTTPException(401, "Incorrect email or password")

        token = create_access_token(subject=user.email, role=user.role)
        return TokenResponse(access_token=token)
