from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.embedding import Embedding
from app.rag.retrievers.retrieval_config import RetrievalConfig
from app.rag.retrievers.retrieval_result import RetrievalResult


class BM25Retriever:
    """
    PostgreSQL Full-Text Search Retriever
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:

        top_k = top_k or RetrievalConfig.DEFAULT_TOP_K

        ts_query = func.plainto_tsquery("english", query)
        rank = func.ts_rank_cd(Embedding.search_vector, ts_query)

        statement = (
            select(Embedding, rank.label("score"))
            .where(Embedding.search_vector.op("@@")(ts_query))
            .order_by(rank.desc())
            .limit(top_k)
        )

        rows = (await self.db.execute(statement)).all()

        results: list[RetrievalResult] = []

        for record, score in rows:
            results.append(
                RetrievalResult(
                    document_id=record.document_id,
                    chunk_id=record.chunk_id,
                    document_type=record.document_type,
                    chunk_index=record.chunk_index,
                    content=record.content,
                    metadata=record.chunk_metadata,
                    similarity_score=float(score),
                )
            )

        return results