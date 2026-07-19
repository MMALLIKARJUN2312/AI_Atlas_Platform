from app.schemas.news_response import NewsResponse


class NewsService:
    async def get_company_news(self, company_id: int) -> list[NewsResponse]:
        """
        Placeholder implementation.

        This will later be replaced with:
        - NewsAPI
        - GNews
        - Google News RSS
        - Cached database articles
        """

        return []