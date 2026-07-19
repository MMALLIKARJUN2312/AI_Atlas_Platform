from fastapi import APIRouter, Depends

from app.schemas.news_response import NewsResponse
from app.services.news_service import NewsService

router = APIRouter(tags=["News"])

def get_news_service() -> NewsService:
    return NewsService()


@router.get(
    "/companies/{company_id}/news",
    response_model=list[NewsResponse],
)
async def get_company_news(
    company_id: int,
    service: NewsService = Depends(get_news_service),
):
    return await service.get_company_news(company_id)