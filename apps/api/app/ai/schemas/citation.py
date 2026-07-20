from pydantic import BaseModel

class Source(BaseModel):
    """
    A grounded source used to answer an AI question.
    """

    title: str
    source_type: str
    company_id: int | None = None
    url: str | None = None
    chunk_id: str
