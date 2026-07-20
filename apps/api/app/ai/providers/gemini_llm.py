from __future__ import annotations

from google import genai

from app.core.config import settings
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse, GroundingChunk, GroundingSupport
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.providers.base_llm import BaseLLM
from app.ai.providers.llm_config import LLMConfig

class GeminiLLM(BaseLLM):
    """
    Gemini implementation
    """

    def __init__(self, config : LLMConfig):
        self.config = config
        self.client = genai.Client(api_key=settings.LLM_API_KEY)

    def generate(self, request : LLMRequest) -> LLMResponse:
        response = self.client.models.generate_content(model=self.config.model,
            contents=[request.system_prompt, request.user_prompt], config={"temperature" : request.temperature, "max_output_tokens" : request.max_output_tokens}
        )

        return LLMResponse(text = response.text.strip(), model = self.config.model)

    def search(self, query: str, *, temperature: float = 0.2, max_output_tokens: int = 2048) -> GroundedLLMResponse:
        response = self.client.models.generate_content(
            model=self.config.model,
            contents=query,
            config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
                "tools": [{"google_search": {}}],
            },
        )

        candidates = response.candidates or []
        grounding = candidates[0].grounding_metadata if candidates else None

        chunks = [
            GroundingChunk(uri=chunk.web.uri, title=chunk.web.title or "")
            for chunk in (grounding.grounding_chunks or [])
            if grounding and getattr(chunk, "web", None) and chunk.web.uri
        ] if grounding else []

        supports = [
            GroundingSupport(
                text=support.segment.text or "",
                start_index=support.segment.start_index or 0,
                end_index=support.segment.end_index or 0,
                chunk_indices=list(support.grounding_chunk_indices or []),
            )
            for support in (grounding.grounding_supports or [])
            if grounding and getattr(support, "segment", None)
        ] if grounding else []

        return GroundedLLMResponse(text=(response.text or "").strip(), model=self.config.model, chunks=chunks, supports=supports)