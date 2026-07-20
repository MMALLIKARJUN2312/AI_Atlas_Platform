from __future__ import annotations

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.database.models.user import User
from app.database.session import AsyncSessionLocal


async def ensure_bootstrap_admin() -> None:
    """Idempotently create the configured admin user if it doesn't exist yet.

    Lets a clean clone log in immediately with ADMIN_EMAIL/ADMIN_PASSWORD
    without a manual seed step.
    """
    async with AsyncSessionLocal() as db:
        existing = await db.scalar(select(User).where(User.email == settings.ADMIN_EMAIL))
        if existing:
            return

        db.add(User(
            email=settings.ADMIN_EMAIL,
            full_name="Admin",
            hashed_password=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        ))
        await db.commit()
