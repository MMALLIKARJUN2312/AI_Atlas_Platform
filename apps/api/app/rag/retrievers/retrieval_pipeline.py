from __future__ import annotations

from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.semantic_retriever import SemanticRetriever

class RetrievalPipeline:
    """
    End to end retrieval pipeline
    """
    
    def __init__(self, retriever : SemanticRetriever, context_builder : ContextBuilder):
        self.retriever = retriever
        self.context_builder = context_builder
    
    def retrieve_context(self, query : str) -> str:
        results = self.retriever.retrieve(query)
        
        return self.context_builder.build(results)