from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.services.news_scheduler import NewsRefreshScheduler

configure_logging()

@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = None
    if settings.NEWS_SCHEDULER_ENABLED:
        scheduler = NewsRefreshScheduler(settings.NEWS_REFRESH_INTERVAL_MINUTES * 60)
        scheduler.start()
    yield
    if scheduler is not None:
        await scheduler.stop()


app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
