from __future__ import annotations

from app.ai.providers.base_llm import BaseLLM
from app.ai.providers.gemini_llm import GeminiLLM
from app.ai.providers.llm_config import LLMConfig

class LLMFactory:
    """
    Creates the configured LLM provider
    """
    
    @staticmethod
    def create(config : LLMConfig) -> BaseLLM:
    
        if config.provider.lower() == "gemini":
            return GeminiLLM(config)
        
        raise ValueError(f"Unsupported LLM provider : {config.provider}")
    