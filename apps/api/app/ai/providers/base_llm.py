from __future__ import annotations

from abc import ABC, abstractmethod

from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse

class BaseLLM(ABC):
    """
    Base interface for all LLM providers
    """
    
    @abstractmethod
    def generate(self, request : LLMRequest) -> LLMResponse:
        """
        Generate a response from the LLM
        """
        raise NotImplementedError
    
    
        