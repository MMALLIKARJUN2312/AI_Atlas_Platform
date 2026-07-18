from __future__ import annotations

from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.vector_store.pgvector_store import PGVectorStore
from app.rag.retrievers.retrieval_config import RetrievalConfig
from app.rag.retrievers.retrieval_result import RetrievalResult

class SemanticRetriever:
    """
    Semantic retrieval using pgvector cosine similarity
    """
    
    def __init__(self, embedding_service : EmbeddingService, vector_store : PGVectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        
    def retrieve(self, query : str, top_k : int | None = None) -> list[RetrievalResult]:
        top_k = top_k or RetrievalConfig.DEFAULT_TOP_K
        query_embedding = self.embedding_service.embed_query(query)
        rows = self.vector_store.similarity_search(embedding=query_embedding, top_k=top_k)
        
        results : list[RetrievalResult] = []
        
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
    