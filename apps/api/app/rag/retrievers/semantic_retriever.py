from __future__ import annotations

import logging

from app.ai.providers.rate_limit import is_rate_limited
from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.retrievers.retrieval_config import RetrievalConfig
from app.rag.retrievers.retrieval_result import RetrievalResult
from app.rag.vector_store.pgvector_store import PGVectorStore

logger = logging.getLogger(__name__)


class SemanticRetriever:
    """
    Semantic retrieval using pgvector cosine similarity.
    """

    def __init__(self, embedding_service: EmbeddingService, vector_store: PGVectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:

        top_k = top_k or RetrievalConfig.DEFAULT_TOP_K

        try:
            query_embedding = self.embedding_service.embed_query(query)
        except Exception as exc:
            # Embedding the query is the one Gemini call every single question
            # makes, so a still-rate-limited provider degrades to "nothing
            # found" here rather than a raw 500 - callers (the knowledge-base
            # tool, /ai/ask) already treat an empty result as an honest miss.
            if not is_rate_limited(exc):
                raise
            logger.warning("Query embedding rate limited, returning empty retrieval for %r", query)
            return []

        rows = await self.vector_store.similarity_search(embedding=query_embedding, top_k=top_k)

        if not rows:
            return []

        # Highest similarity score
        best_score = float(rows[0][1])

        # Reject the entire retrieval if even the best match is weak
        if best_score < RetrievalConfig.MIN_SIMILARITY_SCORE:
            return []

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