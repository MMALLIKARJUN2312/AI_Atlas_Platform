from __future__ import annotations

from abc import ABC, abstractmethod

from app.ai.schemas.grounded_llm_response import GroundedLLMResponse
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse

class BaseLLM(ABC):
    """
    Base interface for all LLM providers
    """

    @abstractmethod
    def generate(self, request : LLMRequest) -> LLMResponse:
        """
        Generate a response from the LLM
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, *, temperature: float = 0.2, max_output_tokens: int = 2048) -> GroundedLLMResponse:
        """
        Generate a response grounded in live web search results.
        """
        raise NotImplementedError
