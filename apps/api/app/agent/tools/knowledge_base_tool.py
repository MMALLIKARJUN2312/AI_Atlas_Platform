from __future__ import annotations

from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.tool_spec import ToolParameter, ToolSpec
from app.ai.services.citation_service import CitationService
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline


class KnowledgeBaseTool(BaseTool):
    """
    Semantic search over the curated knowledge base (companies, sectors,
    problems, problem/company mappings and indexed news).

    This is the RAG path, and it keeps the original 0.60 similarity floor: if
    nothing clears it the tool reports an honest miss rather than handing the
    model weak context it would then dress up as an answer. The difference from
    the old chatbot is what happens next - a miss is now an observation the
    agent can react to (try the web, try the directory), not a dead end.
    """

    def __init__(self, retrieval_pipeline: RetrievalPipeline, citation_service: CitationService):
        self.retrieval_pipeline = retrieval_pipeline
        self.citation_service = citation_service

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="search_knowledge_base",
            description=(
                "Search AI Atlas's curated knowledge base of Food & Beverage AI vendors, "
                "market sectors, industry problems, and company news. Use this FIRST for any "
                "question about specific companies, vendors, sectors, use cases, or problems. "
                "Best for meaning-based questions such as 'which vendors do predictive "
                "maintenance for breweries'."
            ),
            parameters=[
                ToolParameter(
                    name="query",
                    description="A focused natural-language search query describing what to find.",
                    required=True,
                )
            ],
        )

    async def run(self, query: str = "", **_: object) -> ToolResult:
        query = (query or "").strip()
        if not query:
            return ToolResult(observation="No query supplied to the knowledge base search.")

        retrieval = await self.retrieval_pipeline.retrieve(query)

        if not retrieval.results:
            return ToolResult(
                observation=(
                    "No sufficiently relevant material found in the AI Atlas knowledge base "
                    f"for '{query}'. Nothing in the curated dataset clears the relevance "
                    "threshold, so do not answer this from the knowledge base."
                ),
                metadata={"hits": 0, "query": query},
            )

        return ToolResult(
            observation=retrieval.context,
            sources=self.citation_service.build(retrieval.results),
            metadata={
                "hits": len(retrieval.results),
                "query": query,
                "top_score": round(retrieval.results[0].similarity_score, 4),
            },
            grounded=True,
        )
