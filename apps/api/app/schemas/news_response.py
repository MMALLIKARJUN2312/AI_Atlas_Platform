from datetime import datetime

from pydantic import BaseModel

class NewsResponse(BaseModel):
    id: str
    title: str
    summary: str
    source: str
    url: str
    published_at: datetime