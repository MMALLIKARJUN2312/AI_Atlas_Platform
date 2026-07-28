from __future__ import annotations

import logging

from app.agent.agent_prompt import AGENT_SYSTEM_PROMPT
from app.agent.schemas import AgentResponse, AgentStep
from app.agent.tool_registry import ToolRegistry
from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import AgentMessage
from app.ai.services.llm_service import LLMService

logger = logging.getLogger(__name__)

DEFAULT_MAX_ITERATIONS = 5


class AgentService:
    """
    The reason-and-act loop.

    Each iteration asks the model what to do next given everything observed so
    far. If it asks for tools, we execute them ourselves and feed the results
    back as observations; if it answers, we stop. The model never touches the
    database or the web directly - it only ever chooses, and we execute. That
    separation is what keeps the agent auditable: every external effect it had
    is in `steps`.

    The loop is bounded. Without a ceiling, a confused model can ping-pong
    between tools indefinitely on one HTTP request, so after
    `max_iterations` we stop calling tools and force a final answer from
    whatever was gathered - a degraded answer beats a hung request.
    """

    def __init__(
        self,
        llm_service: LLMService,
        registry: ToolRegistry,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ):
        self.llm_service = llm_service
        self.registry = registry
        self.max_iterations = max_iterations

    async def ask(self, question: str) -> AgentResponse:
        messages: list[AgentMessage] = [AgentMessage(role="user", text=question)]
        steps: list[AgentStep] = []
        sources: list[Source] = []
        tools_used: list[str] = []
        grounded = False
        answer = ""
        iterations = 0

        for iteration in range(1, self.max_iterations + 1):
            iterations = iteration
            # On the final iteration we withdraw the tools entirely, which is
            # what forces the model to commit to an answer instead of asking
            # for yet another lookup we would have to ignore.
            last_iteration = iteration == self.max_iterations
            response = self.llm_service.generate_with_tools(
                messages=messages,
                tools=[] if last_iteration else self.registry.specs,
                system_prompt=AGENT_SYSTEM_PROMPT,
            )

            if not response.invocations:
                answer = response.text
                break

            messages.append(AgentMessage(role="model", invocations=response.invocations))

            for invocation in response.invocations:
                result = await self.registry.execute(invocation.name, invocation.arguments)

                steps.append(
                    AgentStep(
                        step=len(steps) + 1,
                        tool=invocation.name,
                        arguments=invocation.arguments,
                        observation=result.observation,
                        metadata=result.metadata,
                    )
                )
                if invocation.name not in tools_used:
                    tools_used.append(invocation.name)
                sources.extend(result.sources)
                grounded = grounded or result.grounded

                messages.append(
                    AgentMessage(
                        role="tool",
                        tool_name=invocation.name,
                        tool_response={"result": result.observation},
                    )
                )

        if not answer:
            logger.warning("Agent produced no answer after %s iterations", iterations)
            answer = (
                "I wasn't able to complete that request. Please try rephrasing your question."
            )

        return AgentResponse(
            answer=answer,
            sources=self._dedupe(sources),
            steps=steps,
            tools_used=tools_used,
            iterations=iterations,
            grounded=grounded,
        )

    @staticmethod
    def _dedupe(sources: list[Source]) -> list[Source]:
        seen: set[str] = set()
        unique: list[Source] = []
        for source in sources:
            if source.chunk_id in seen:
                continue
            seen.add(source.chunk_id)
            unique.append(source)
        return unique
