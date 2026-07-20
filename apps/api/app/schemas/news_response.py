from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str
    source_name: str
    source_url: str
    published_at: datetime


class CompanyNewsResponse(BaseModel):
    articles: list[NewsResponse]


class NewsRefreshResponse(CompanyNewsResponse):
    added_count: int
