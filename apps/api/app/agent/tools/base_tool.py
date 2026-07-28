from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import ToolSpec


class ToolResult(BaseModel):
    """
    The outcome of running one tool.

    `observation` is what the model sees next step. `sources` are the real,
    traceable citations behind that observation - they travel separately so a
    tool can never bury a fake citation inside free text, and so the API can
    show the user exactly what the answer was built from.
    """

    observation: str
    sources: list[Source] = []
    metadata: dict[str, Any] = {}
    grounded: bool = False


class BaseTool(ABC):
    """
    Base class for every capability the agent can invoke.

    A tool is the only way the agent is allowed to touch the outside world -
    the database, the vector store, or the live web. Everything else it does is
    pure reasoning over tool observations.
    """

    @property
    @abstractmethod
    def spec(self) -> ToolSpec:
        """What the model is told about this tool."""
        raise NotImplementedError

    @abstractmethod
    async def run(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with model-supplied arguments."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.spec.name
