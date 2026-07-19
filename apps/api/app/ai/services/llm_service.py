from __future__ import annotations

from app.ai.providers.base_llm import BaseLLM
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.services.response_validator import ResponseValidator


class LLMService:
    """
    Central service for all LLM interactions
    """

    def __init__(self, llm: BaseLLM, validator: ResponseValidator):
        self.llm = llm
        self.validator = validator

    def generate(self, request : LLMRequest) -> LLMResponse:

        response = self.llm.generate(system_prompt=request.system_prompt, user_prompt=request.user_prompt,)

        self.validator.validate(response)

        return response