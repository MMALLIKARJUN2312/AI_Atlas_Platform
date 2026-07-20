from collections.abc import AsyncGenerator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database.models.user import User
from app.database.session import get_db

async def get_database() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session


Database = Annotated[AsyncSession, Depends(get_database)]
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_admin_user(
    db: Database,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None:
        raise HTTPException(401, "Not authenticated", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}) from exc

    user = await db.scalar(select(User).where(User.email == payload.get("sub")))
    if not user or not user.is_active or user.role != "admin":
        raise HTTPException(403, "Admin access required")

    return user