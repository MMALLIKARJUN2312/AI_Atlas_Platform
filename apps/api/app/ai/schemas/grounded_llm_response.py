from pydantic import BaseModel


class GroundingChunk(BaseModel):
    """A single real web search result backing a grounded response."""

    uri: str
    title: str = ""


class GroundingSupport(BaseModel):
    """A span of grounded text and the chunks that back it."""

    text: str
    start_index: int
    end_index: int
    chunk_indices: list[int]


class GroundedLLMResponse(BaseModel):
    """
    Response from an LLM call grounded in live web search, e.g. Gemini's
    Google Search grounding tool. `chunks`/`supports` are empty when the
    provider returned no search results for the query.
    """

    text: str
    model: str
    chunks: list[GroundingChunk] = []
    supports: list[GroundingSupport] = []
