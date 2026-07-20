from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_database
from app.repositories.company_repository import CompanyRepository
from app.repositories.news_repository import NewsRepository
from app.schemas.news_response import CompanyNewsResponse, NewsRefreshResponse
from app.services.news_factory import build_news_service
from app.services.news_service import NewsService

router = APIRouter(tags=["News"])
Database = Annotated[AsyncSession, Depends(get_database)]


def get_news_service(
    db: Database,
) -> NewsService:
    return build_news_service(db)


def get_news_read_service(db: Database) -> NewsService:
    return NewsService(NewsRepository(db), CompanyRepository(db))


Service = Annotated[NewsService, Depends(get_news_service)]
ReadService = Annotated[NewsService, Depends(get_news_read_service)]


@router.get("/companies/{company_id}/news", response_model=CompanyNewsResponse)
async def get_company_news(company_id: int, service: ReadService):
    articles = await service.get_company_news(company_id)
    return CompanyNewsResponse(articles=articles)


@router.post("/companies/{company_id}/news/refresh", response_model=NewsRefreshResponse)
async def refresh_company_news(company_id: int, service: Service):
    try:
        added_articles = await service.refresh_company_news(company_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    articles = await service.get_company_news(company_id)
    return NewsRefreshResponse(articles=articles, added_count=len(added_articles))
