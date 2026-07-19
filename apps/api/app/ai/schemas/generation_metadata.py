from pydantic import BaseModel

class GenerationMetadata(BaseModel):
    """
    Metadata associated with a LLM generation
    """
    
    model : str 
    provider : str 
    latency_ms : float | None = None
    prompt_tokens : int | None = None 
    completion_tokens : int | None = None

    
    