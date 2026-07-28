from __future__ import annotations

import logging

from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.tool_spec import ToolSpec

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    The agent's capability surface.

    Registering a tool is the only way to extend what the agent can do, which
    keeps one list as the single source of truth for both what the model is
    told it can call and what can actually be executed. A model asking for a
    tool that isn't registered gets a normal error observation instead of an
    exception, so a hallucinated tool name degrades into a recoverable step
    rather than a failed request.
    """

    def __init__(self, tools: list[BaseTool]):
        self._tools: dict[str, BaseTool] = {tool.name: tool for tool in tools}

    @property
    def specs(self) -> list[ToolSpec]:
        return [tool.spec for tool in self._tools.values()]

    @property
    def names(self) -> list[str]:
        return list(self._tools)

    async def execute(self, name: str, arguments: dict) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            logger.warning("Agent requested unknown tool %r", name)
            return ToolResult(
                observation=(
                    f"'{name}' is not an available tool. Available tools: {', '.join(self._tools)}. "
                    "Choose one of these instead."
                ),
                metadata={"error": "unknown_tool"},
            )

        try:
            return await tool.run(**arguments)
        except TypeError as exc:
            logger.warning("Bad arguments for tool %r: %s", name, exc)
            return ToolResult(
                observation=f"Invalid arguments for '{name}': {exc}. Retry with corrected arguments.",
                metadata={"error": "bad_arguments"},
            )
        except Exception:
            logger.exception("Tool %r failed", name)
            return ToolResult(
                observation=(
                    f"The '{name}' tool failed to execute. Do not invent its result - "
                    "either try a different tool or tell the user this lookup failed."
                ),
                metadata={"error": "tool_failed"},
            )
