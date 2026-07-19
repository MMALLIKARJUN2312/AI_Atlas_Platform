from fastapi import APIRouter
from fastapi import Depends

from app.ai.services.ask_ai_service import AskAIService
from app.ai.schemas.ask_ai_request import AskAIRequest
from app.ai.schemas.ask_ai_response import AskAIResponse

from app.api.deps_ai import get_ask_ai_service

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/ask",
    response_model=AskAIResponse,
)
async def ask_ai(
    request : AskAIRequest,
    service : AskAIService = Depends(get_ask_ai_service),
):

    return await service.ask(request.question)