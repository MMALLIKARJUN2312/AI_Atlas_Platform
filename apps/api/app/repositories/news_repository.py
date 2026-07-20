from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.news import News
from app.repositories.base_repository import BaseRepository


class NewsRepository(BaseRepository[News]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, News)

    async def get_company_news(self, company_id: int, *, limit: int = 50, offset: int = 0) -> list[News]:
        statement = (
            select(News)
            .where(News.company_id == company_id)
            .order_by(News.published_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(await self.db.scalars(statement))

    async def create_news(self, news: News) -> News:
        self.db.add(news)
        await self.db.commit()
        await self.db.refresh(news)
        return news

    async def bulk_create_news(self, news_items: list[News]) -> list[News]:
        if not news_items:
            return []
        self.db.add_all(news_items)
        await self.db.commit()
        for item in news_items:
            await self.db.refresh(item)
        return news_items

    async def exists_by_url(self, url: str) -> bool:
        statement = select(News.id).where(News.source_url == url).limit(1)
        return await self.db.scalar(statement) is not None
