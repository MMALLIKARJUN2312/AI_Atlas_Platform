from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.ai.schemas.citation import Source


class AgentRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AgentStep(BaseModel):
    """
    One observable step of the agent's reasoning.

    Exposed to the client on purpose: an agent that silently decides what to do
    is impossible to debug or trust, and being able to see "it searched the KB,
    found nothing, then went to the web" is what makes the behaviour reviewable
    by a human.
    """

    step: int
    tool: str
    arguments: dict[str, Any] = {}
    observation: str
    metadata: dict[str, Any] = {}


class AgentResponse(BaseModel):
    answer: str
    sources: list[Source] = []
    steps: list[AgentStep] = []
    tools_used: list[str] = []
    iterations: int = 0
    grounded: bool = False
