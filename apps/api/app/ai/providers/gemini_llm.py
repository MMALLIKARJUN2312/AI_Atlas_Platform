from __future__ import annotations

from google import genai
from google.genai import types

from app.core.config import settings
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse, GroundingChunk, GroundingSupport
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.schemas.tool_spec import AgentMessage, ToolAwareResponse, ToolInvocation, ToolSpec
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
        One reasoning step of the agent loop, using Gemini function calling.

        Automatic function calling is explicitly disabled: we want the model to
        *declare* which tool it wants, and then execute it ourselves. That keeps
        every tool call observable, auditable, and testable - the SDK silently
        running our database code in a hidden loop would make the agent
        impossible to reason about in production.
        """
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_prompt,
            tools=[types.Tool(function_declarations=[self._declaration(tool) for tool in tools])] if tools else None,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )

        response = self.client.models.generate_content(
            model=self.config.model,
            contents=[self._content(message) for message in messages],
            config=config,
        )

        invocations = [
            ToolInvocation(
                name=part.function_call.name,
                arguments=dict(part.function_call.args or {}),
                provider_signature=part.thought_signature,
            )
            for candidate in (response.candidates or [])
            for part in (candidate.content.parts or [] if candidate.content else [])
            if part.function_call and part.function_call.name
        ]

        return ToolAwareResponse(
            text=self._safe_text(response),
            invocations=invocations,
            model=self.config.model,
        )

    @staticmethod
    def _safe_text(response) -> str:
        """
        `response.text` raises when the candidate contains only function calls
        and no text part, which is the normal case mid-loop.
        """
        try:
            return (response.text or "").strip()
        except (AttributeError, ValueError):
            return ""

    @staticmethod
    def _declaration(tool: ToolSpec) -> types.FunctionDeclaration:
        properties = {
            parameter.name: types.Schema(
                type=parameter.type.upper(),
                description=parameter.description,
            )
            for parameter in tool.parameters
        }
        return types.FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters=types.Schema(
                type="OBJECT",
                properties=properties,
                required=[parameter.name for parameter in tool.parameters if parameter.required],
            ) if properties else None,
        )

    @staticmethod
    def _content(message: AgentMessage) -> types.Content:
        if message.role == "tool":
            return types.Content(
                role="user",
                parts=[types.Part.from_function_response(
                    name=message.tool_name or "unknown_tool",
                    response=message.tool_response or {},
                )],
            )

        if message.role == "model" and message.invocations:
            return types.Content(
                role="model",
                parts=[
                    types.Part(
                        function_call=types.FunctionCall(name=invocation.name, args=invocation.arguments),
                        thought_signature=invocation.provider_signature,
                    )
                    for invocation in message.invocations
                ],
            )

        return types.Content(
            role="model" if message.role == "model" else "user",
            parts=[types.Part.from_text(text=message.text or " ")],
        )