from __future__ import annotations

from google import genai

from app.core.config import settings
from app.ai.providers.base_llm import BaseLLM

class GeminiLLM(BaseLLM):
    """
    Gemini implementation of BaseLLM
    """
    
    def __init__(self, model : str):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.mode = model
        
    def generate(self, *, system_prompt : str, user_prompt : str) -> str:
        response = self.client.models.generate_content(model=self.model, contents=[system_prompt, user_prompt])
    
        return response.text.strip()