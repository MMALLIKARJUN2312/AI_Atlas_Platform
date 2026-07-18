from __future__ import annotations

from app.rag.retrievers.retrieval_result import RetrievalResult

class ContextBuilder:
    """
    Converts retrieval result to LLM context
    """
    
    def build(self, results : list[RetrievalResult]) -> str:
        sections = []
        
        for result in results:
            sections.append(result.content)
            
        return "\n\n".join(sections)
    