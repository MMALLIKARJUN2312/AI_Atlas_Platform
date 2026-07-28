from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class ToolParameter(BaseModel):
    """
    One argument a tool accepts.

    Deliberately provider-neutral: this is our own vocabulary, and each LLM
    provider adapter is responsible for translating it into whatever function
    -calling schema that provider expects. Swapping Gemini for another model
    means writing one adapter, not rewriting every tool.
    """

    name: str
    description: str
    type: Literal["string", "integer", "number", "boolean"] = "string"
    required: bool = False


class ToolSpec(BaseModel):
    """
    The contract the model sees for a tool: what it is called, when to use it,
    and what it accepts. The description is the only thing steering the model's
    choice, so it states *when* to reach for the tool, not just what it does.
    """

    name: str
    description: str
    parameters: list[ToolParameter] = []


class ToolInvocation(BaseModel):
    """A model's request to run one tool with concrete arguments."""

    name: str
    arguments: dict[str, Any] = {}
    # Gemini's "thinking" models attach a signature to each function-call part
    # that must be echoed back verbatim when the call is replayed into the
    # next turn's history, or the API rejects the request. Opaque outside the
    # provider adapter - other providers simply leave this unset.
    provider_signature: bytes | None = None


class AgentMessage(BaseModel):
    """
    One turn in the agent's working conversation.

    'tool' messages carry the observation produced by executing a tool, which
    is fed back to the model so the next step can reason over real data.
    """

    role: Literal["user", "model", "tool"]
    text: str = ""
    invocations: list[ToolInvocation] = []
    tool_name: str | None = None
    tool_response: dict[str, Any] | None = None


class ToolAwareResponse(BaseModel):
    """
    A model response that either answers directly (text, no invocations) or
    asks to call one or more tools first (invocations populated).
    """

    text: str = ""
    invocations: list[ToolInvocation] = []
    model: str = ""
