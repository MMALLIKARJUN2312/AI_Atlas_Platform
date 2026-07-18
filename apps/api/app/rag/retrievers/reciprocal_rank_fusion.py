from __future__ import annotations

from collections import defaultdict

from app.rag.retrievers.retrieval_result import RetrievalResult

class ReciprocalRankFusion:
    """
    Combines ranked lists from multiple retrievers
    """
    
    def __init__(self, k : int = 60):
        self.k = k 
        
    def fuse(self, ranked_lists : list[list[RetrievalResult]]) -> list[RetrievalResult] :
        scores = defaultdict(float)
        lookup = {}
        
        for results in ranked_lists:
            for rank, result in enumerate(results, start=1):
                key = result.chunk_id
                lookup[key] = result
                scores[key] += 1.0 / (self.k + rank)
                
        fused = sorted(lookup.values(), key=lambda item:scores[item.chunk_id], reverse=True)
        
        return fused 