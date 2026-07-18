from __future__ import annotations

from app.rag.retrievers.bm25_retriever import BM25Retriever
from app.rag.retrievers.reciprocal_rank_fusion import ReciprocalRankFusion
from app.rag.retrievers.retrieval_result import RetrievalResult
from app.rag.retrievers.semantic_retriever import SemanticRetriever

class HybridRetriever:
    """
    Combines semantic retrieval and BM25 retrieval
    """
    
    def __init__(self, semantic_retriever : SemanticRetriever, bm25_retriever : BM25Retriever, fusion : ReciprocalRankFusion):
        self.semantic_retriever = semantic_retriever
        self.bm25_recruiter = bm25_retriever
        self.fusion = fusion
        
    def retrieve(self, query : str, top_k : int = 10) -> list[RetrievalResult]:
        semantic_results = self.semantic_retriever.retrieve(query, top_k)
        bm25_results = self.bm25_recruiter.retrieve(query, top_k)

        return self.fusion.fuse([semantic_results, bm25_results])[:top_k]