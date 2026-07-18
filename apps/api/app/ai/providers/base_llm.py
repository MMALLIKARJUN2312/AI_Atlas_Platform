from __future__ import annotations

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """
    Base interface for all LLMs
    """
    
    @abstractmethod
    def generate(self, *, system_prompt : str, user_prompt : str) -> str:
        """
        Generate a response from the LLM
        """
        raise NotImplementedError
    
    
        