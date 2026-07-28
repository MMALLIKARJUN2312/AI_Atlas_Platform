from __future__ import annotations

from app.ai.providers.base_llm import BaseLLM
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.schemas.tool_spec import AgentMessage, ToolAwareResponse, ToolSpec
from app.ai.services.response_validator import ResponseValidator


class LLMService:
    """
    Central service for all LLM interactions
    """

    def __init__(self, llm: BaseLLM, validator: ResponseValidator):
        self.llm = llm
        self.validator = validator

    def generate(self, request : LLMRequest) -> LLMResponse:

        response = self.llm.generate(request=request)

        self.validator.validate(response)

        return response

    def search(self, query: str) -> GroundedLLMResponse:
        """Generate a response grounded in live web search results."""

        return self.llm.search(query)

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
        One tool-enabled reasoning step for the agent.

        Intentionally not passed through ResponseValidator: mid-loop responses
        legitimately carry no text at all (only function calls), which the
        validator would reject as an empty completion. The agent's grounding
        guarantees come from the tools and the final-answer rules instead.
        """

        return self.llm.generate_with_tools(
            messages=messages,
            tools=tools,
            system_prompt=system_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )