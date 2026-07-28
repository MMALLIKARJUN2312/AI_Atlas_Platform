from __future__ import annotations

from abc import ABC, abstractmethod

from app.ai.schemas.grounded_llm_response import GroundedLLMResponse
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.schemas.tool_spec import AgentMessage, ToolAwareResponse, ToolSpec

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

    @abstractmethod
    def generate_with_tools(
        self,
        messages: list[AgentMessage],
        tools: list[ToolSpec],
        *,
        system_prompt: str,
        temperature: float = 0.1,
        max_output_tokens: int = 2048,
    ) -> ToolAwareResponse:
        """
        Run one reasoning step with tools available.

        Returns either a final answer (text, no invocations) or the tools the
        model wants executed before it can answer. Driving the loop is the
        agent's job, not the provider's - the provider only reports what the
        model decided this step.
        """
        raise NotImplementedError
