from __future__ import annotations

from google import genai

from app.core.config import settings
from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.providers.base_llm import BaseLLM
from app.ai.providers.llm_config import LLMConfig

class GeminiLLM(BaseLLM):
    """
    Gemini implementation
    """
    
    def __init__(self, config : LLMConfig):
        self.config = config
        self.client = genai.Client(api_key=settings.LLM_API_KEY)
        
    def generate(self, request : LLMRequest) -> LLMResponse:
        response = self.client.models.generate_content(model=self.config.model, 
            contents=[request.system_prompt, request.user_prompt], config={"temperature" : request.temperature, "max_output_tokens" : request.max_output_tokens}
        )
    
        return LLMResponse(text = response.text.strip(), model = self.config.model)