from __future__ import annotations

from app.ai.providers.base_llm import BaseLLM
from app.ai.providers.gemini_llm import GeminiLLM

class LLMFactory:
    """
    Creates the configured LLM provider
    """
    
    @staticmethod
    def create(provider : str, model : str) -> BaseLLM:
        provider = provider.lower()
        
        if provider == "gemini":
            return GeminiLLM(model)
        
        raise ValueError(f"Unsupported LLM provider : {provider}")
    