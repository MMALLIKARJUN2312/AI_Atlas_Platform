import pytest

from app.agent.tool_registry import ToolRegistry
from app.agent.tools.base_tool import BaseTool, ToolResult
from app.ai.schemas.tool_spec import ToolSpec


class EchoTool(BaseTool):
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(name="echo", description="echoes its argument")

    async def run(self, message: str) -> ToolResult:
        return ToolResult(observation=message)


class ExplodingTool(BaseTool):
    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(name="exploding", description="always fails")

    async def run(self, **kwargs) -> ToolResult:
        raise RuntimeError("boom")


def test_specs_and_names_reflect_registered_tools():
    registry = ToolRegistry([EchoTool()])
    assert registry.names == ["echo"]
    assert registry.specs[0].name == "echo"


@pytest.mark.asyncio
async def test_execute_runs_the_named_tool_with_arguments():
    registry = ToolRegistry([EchoTool()])
    result = await registry.execute("echo", {"message": "hi"})
    assert result.observation == "hi"


@pytest.mark.asyncio
async def test_execute_unknown_tool_returns_recoverable_result_not_an_exception():
    registry = ToolRegistry([EchoTool()])
    result = await registry.execute("does_not_exist", {})
    assert "not an available tool" in result.observation
    assert "echo" in result.observation
    assert result.metadata["error"] == "unknown_tool"


@pytest.mark.asyncio
async def test_execute_bad_arguments_returns_recoverable_result():
    registry = ToolRegistry([EchoTool()])
    result = await registry.execute("echo", {"wrong_argument": "hi"})
    assert result.metadata["error"] == "bad_arguments"


@pytest.mark.asyncio
async def test_execute_tool_exception_is_contained():
    registry = ToolRegistry([ExplodingTool()])
    result = await registry.execute("exploding", {})
    assert result.metadata["error"] == "tool_failed"
    assert "Do not invent" in result.observation
