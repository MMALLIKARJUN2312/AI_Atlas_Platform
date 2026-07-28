from fastapi import APIRouter, Depends

from app.agent.agent_service import AgentService
from app.agent.schemas import AgentRequest, AgentResponse
from app.api.deps_ai import get_agent_service

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/ask", response_model=AgentResponse)
async def ask_agent(
    request: AgentRequest,
    service: AgentService = Depends(get_agent_service),
):
    """
    Ask the AI Atlas agent.

    Unlike /ai/ask (single-shot RAG), the agent decides which capabilities to
    use, can chain several, and returns the reasoning trace alongside the
    answer so the caller can see exactly how it was produced.
    """
    return await service.ask(request.question)
