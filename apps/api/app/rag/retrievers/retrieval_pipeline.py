from __future__ import annotations

from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.retrieval_output import RetrievalOutput
from app.rag.retrievers.hybrid_retriever import HybridRetriever

class RetrievalPipeline:
    """
    End to end retrieval pipeline
    """
    
    def __init__(self, retriever : HybridRetriever, context_builder : ContextBuilder):
        self.retriever = retriever
        self.context_builder = context_builder
    
    async def retrieve(self, query : str) -> RetrievalOutput:
        results = await self.retriever.retrieve(query)
        context = self.context_builder.build(results)
        
        print("=" * 80)
        print("CONTEXT")
        print(context)
        print("=" * 80)
        
        return RetrievalOutput(context=context, results=results)