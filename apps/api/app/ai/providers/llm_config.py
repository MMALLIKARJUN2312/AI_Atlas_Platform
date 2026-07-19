from dataclasses import dataclass

@dataclass(frozen=True)
class LLMConfig:
    provider : str 
    model : str 
    api_key : str | None = None