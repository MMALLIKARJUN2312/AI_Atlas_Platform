from __future__ import annotations

from app.ai.schemas.citation import Citation
from app.rag.retrievers.retrieval_result import RetrievalResult

class CitationService:
    """
    Builds citations from retrieved chunks
    """
    
    def build(self, results : list[RetrievalResult]) -> list[Citation]:
        citations = []
        
        seen : set[tuple[str, str]] = set()
        
        for result in results:
            key = (result.document_id, result.chunk_id)
            
            if key in seen:
                continue
            
            seen.add(key)
            
            citations.append(
                Citation(
                    document_id=result.document_id, 
                    chunk_id=result.document_id, 
                    document_type=result.document_type,
                )
            )
            
        return citations