from __future__ import annotations

import logging

from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.providers.rate_limit import is_rate_limited
from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import ToolParameter, ToolSpec
from app.ai.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class WebSearchTool(BaseTool):
    """
    Live, grounded web search for questions the curated dataset cannot answer.

    Two things make this safe to expose to the agent. First, it is grounded
    search, so every claim comes back with real source URIs we surface as
    citations rather than the model free-associating from memory. Second, its
    results are clearly labelled as external in the observation, so the final
    answer can tell the user which parts came from AI Atlas's verified
    directory and which came from the open web.

    The provider's grounding quota is far stricter than plain generation, so a
    rate-limit here degrades to an honest "couldn't reach live search" rather
    than failing the whole request - the agent can still answer from whatever
    it already retrieved.
    """

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="web_search",
            description=(
                "Search the live web for current, general, or external information that is NOT "
                "in the AI Atlas knowledge base. Use this only after the knowledge base has "
                "been tried and came back empty, or for general industry questions, definitions, "
                "regulations, or recent events beyond the curated directory."
            ),
            parameters=[
                ToolParameter(
                    name="query",
                    description="The web search query.",
                    required=True,
                )
            ],
        )

    async def run(self, query: str = "", **_: object) -> ToolResult:
        query = (query or "").strip()
        if not query:
            return ToolResult(observation="No query supplied to web search.")

        try:
            grounded = self.llm_service.search(query)
        except Exception as exc:
            logger.warning("Live web search unavailable for %r: %s", query, exc)
            if is_rate_limited(exc):
                return ToolResult(
                    observation=(
                        "Live web search is temporarily unavailable (provider rate limit). "
                        "Answer from knowledge-base results if you have them, and tell the user "
                        "live web lookup could not be performed right now."
                    ),
                    metadata={"error": "rate_limited"},
                )
            return ToolResult(
                observation="Live web search failed. Do not fabricate external information.",
                metadata={"error": "search_failed"},
            )

        if not grounded.text:
            return ToolResult(
                observation=f"Live web search returned no usable results for '{query}'.",
                metadata={"results": 0},
            )

        sources = [
            Source(
                title=chunk.title or chunk.uri,
                source_type="web",
                url=chunk.uri,
                chunk_id=f"web:{index}",
            )
            for index, chunk in enumerate(grounded.chunks)
            if chunk.uri
        ]

        return ToolResult(
            observation=(
                "EXTERNAL WEB RESULT (not from the curated AI Atlas directory - "
                "attribute it as external information):\n"
                f"{grounded.text}"
            ),
            sources=sources,
            metadata={"results": len(sources), "query": query},
            grounded=bool(sources),
        )
