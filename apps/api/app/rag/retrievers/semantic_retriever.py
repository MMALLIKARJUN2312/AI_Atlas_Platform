from __future__ import annotations

from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.retrievers.retrieval_config import RetrievalConfig
from app.rag.retrievers.retrieval_result import RetrievalResult
from app.rag.vector_store.pgvector_store import PGVectorStore


class SemanticRetriever:
    """
    Semantic retrieval using pgvector cosine similarity.
    """

    def __init__(self, embedding_service: EmbeddingService, vector_store: PGVectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievalResult]:

        top_k = top_k or RetrievalConfig.DEFAULT_TOP_K

        query_embedding = self.embedding_service.embed_query(query)

        rows = await self.vector_store.similarity_search(embedding=query_embedding, top_k=top_k)

        print("=" * 80)
        print("Retrieved rows:", len(rows))

        for record, score in rows:
            print(record.chunk_id)
            print(record.document_id)
            print(score)
            print(record.content[:200])
            print("-" * 40)

        if not rows:
            return []

        # Highest similarity score
        best_score = float(rows[0][1])

        print(f"Best similarity score: {best_score}")

        # Reject the entire retrieval if even the best match is weak
        if best_score < RetrievalConfig.MIN_SIMILARITY_SCORE:
            print(
                f"No relevant context found. "
                f"Best score ({best_score:.4f}) "
                f"is below threshold ({RetrievalConfig.MIN_SIMILARITY_SCORE})."
            )
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