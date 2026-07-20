from __future__ import annotations

import asyncio
import logging

from app.database.session import AsyncSessionLocal
from app.repositories.company_repository import CompanyRepository
from app.services.news_factory import build_news_service

logger = logging.getLogger(__name__)


class NewsRefreshScheduler:
    """In-process periodic refresh for a single API-worker deployment."""

    def __init__(self, interval_seconds: int):
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _run(self) -> None:
        while True:
            await self.refresh_all()
            await asyncio.sleep(self.interval_seconds)

    async def refresh_all(self) -> None:
        async with AsyncSessionLocal() as db:
            companies = await CompanyRepository(db).find_all()
            for company in companies:
                try:
                    await build_news_service(db).refresh_company_news(company.id)
                except Exception:
                    logger.exception("Scheduled news refresh failed for company_id=%s", company.id)
