import pytest

from app.agent.agent_service import AgentService
from app.agent.tool_registry import ToolRegistry
from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.citation import Source
from app.ai.schemas.tool_spec import ToolAwareResponse, ToolInvocation, ToolSpec
from app.ai.services.llm_service import LLMService


class FakeTool(BaseTool):
    """A tool whose observation and sources are canned per test."""

    def __init__(self, name: str, observation: str, sources: list[Source] | None = None, grounded: bool = True):
        self._name = name
        self._observation = observation
        self._sources = sources or []
        self._grounded = grounded
        self.calls: list[dict] = []

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(name=self._name, description="test tool")

    async def run(self, **kwargs) -> ToolResult:
        self.calls.append(kwargs)
        return ToolResult(observation=self._observation, sources=self._sources, grounded=self._grounded)


class ScriptedLLM:
    """
    Stands in for LLMService.generate_with_tools: returns a scripted sequence
    of ToolAwareResponse objects, one per call, so a test can dictate exactly
    how the model behaves at each step of the reason-act loop.
    """

    def __init__(self, responses: list[ToolAwareResponse]):
        self._responses = list(responses)
        self.calls: list[list] = []

    def generate_with_tools(self, messages, tools, **kwargs):
        self.calls.append(tools)
        return self._responses.pop(0)


def _as_llm_service(scripted: ScriptedLLM) -> LLMService:
    # AgentService only calls generate_with_tools, so a bare object with that
    # method is enough - no need to construct a real LLMService/BaseLLM.
    return scripted  # type: ignore[return-value]


@pytest.mark.asyncio
async def test_agent_answers_directly_when_no_tool_is_needed():
    llm = ScriptedLLM([ToolAwareResponse(text="Hello! How can I help?", invocations=[])])
    registry = ToolRegistry([])
    agent = AgentService(_as_llm_service(llm), registry)

    result = await agent.ask("hi")

    assert result.answer == "Hello! How can I help?"
    assert result.tools_used == []
    assert result.iterations == 1
    assert result.grounded is False


@pytest.mark.asyncio
async def test_agent_executes_a_requested_tool_and_feeds_the_observation_back():
    kb_tool = FakeTool(
        "search_knowledge_base",
        observation="Krones makes bottling lines.",
        sources=[Source(title="Krones", source_type="company", chunk_id="c1")],
    )
    llm = ScriptedLLM([
        ToolAwareResponse(invocations=[ToolInvocation(name="search_knowledge_base", arguments={"query": "Krones"})]),
        ToolAwareResponse(text="Krones makes bottling lines for the beverage industry."),
    ])
    registry = ToolRegistry([kb_tool])
    agent = AgentService(_as_llm_service(llm), registry)

    result = await agent.ask("What does Krones make?")

    assert kb_tool.calls == [{"query": "Krones"}]
    assert result.answer == "Krones makes bottling lines for the beverage industry."
    assert result.tools_used == ["search_knowledge_base"]
    assert result.iterations == 2
    assert result.grounded is True
    assert len(result.sources) == 1
    assert result.steps[0].tool == "search_knowledge_base"
    assert result.steps[0].observation == "Krones makes bottling lines."


@pytest.mark.asyncio
async def test_agent_chains_multiple_tools_across_iterations():
    empty_kb = FakeTool("search_knowledge_base", observation="No hits.", grounded=False)
    web = FakeTool(
        "web_search",
        observation="EXTERNAL: HACCP is a food safety framework.",
        sources=[Source(title="Wikipedia", source_type="web", chunk_id="w1")],
    )
    llm = ScriptedLLM([
        ToolAwareResponse(invocations=[ToolInvocation(name="search_knowledge_base", arguments={"query": "HACCP"})]),
        ToolAwareResponse(invocations=[ToolInvocation(name="web_search", arguments={"query": "HACCP"})]),
        ToolAwareResponse(text="HACCP is a food safety framework (external source)."),
    ])
    registry = ToolRegistry([empty_kb, web])
    agent = AgentService(_as_llm_service(llm), registry)

    result = await agent.ask("What is HACCP?")

    assert result.tools_used == ["search_knowledge_base", "web_search"]
    assert result.iterations == 3
    assert len(result.steps) == 2
    assert result.grounded is True  # the web tool's result was grounded even though KB's wasn't


@pytest.mark.asyncio
async def test_agent_requesting_an_unknown_tool_gets_a_recoverable_observation():
    llm = ScriptedLLM([
        ToolAwareResponse(invocations=[ToolInvocation(name="not_a_real_tool", arguments={})]),
        ToolAwareResponse(text="I couldn't find that information."),
    ])
    registry = ToolRegistry([FakeTool("search_knowledge_base", observation="irrelevant")])
    agent = AgentService(_as_llm_service(llm), registry)

    result = await agent.ask("do something odd")

    assert result.answer == "I couldn't find that information."
    assert "not an available tool" in result.steps[0].observation


@pytest.mark.asyncio
async def test_agent_stops_and_forces_an_answer_at_the_iteration_ceiling():
    """
    A model that keeps asking for tools forever must not hang the request -
    the loop withdraws tools on the final iteration, forcing a text answer.
    """
    tool = FakeTool("search_knowledge_base", observation="some context")
    always_calls_tool = [
        ToolAwareResponse(invocations=[ToolInvocation(name="search_knowledge_base", arguments={"query": "x"})])
        for _ in range(2)
    ] + [ToolAwareResponse(text="Best answer I can give given the tools withdrawn.")]
    llm = ScriptedLLM(always_calls_tool)
    registry = ToolRegistry([tool])
    agent = AgentService(_as_llm_service(llm), registry, max_iterations=3)

    result = await agent.ask("keep looping")

    assert result.iterations == 3
    assert result.answer == "Best answer I can give given the tools withdrawn."
    # The final iteration's call must have been made with tools withdrawn.
    assert llm.calls[-1] == []


@pytest.mark.asyncio
async def test_agent_sources_are_deduplicated_across_steps():
    same_source = Source(title="Krones", source_type="company", chunk_id="c1")
    tool = FakeTool("search_knowledge_base", observation="Krones info.", sources=[same_source])
    llm = ScriptedLLM([
        ToolAwareResponse(invocations=[ToolInvocation(name="search_knowledge_base", arguments={"query": "a"})]),
        ToolAwareResponse(invocations=[ToolInvocation(name="search_knowledge_base", arguments={"query": "b"})]),
        ToolAwareResponse(text="done"),
    ])
    registry = ToolRegistry([tool])
    agent = AgentService(_as_llm_service(llm), registry)

    result = await agent.ask("q")

    assert len(result.sources) == 1
