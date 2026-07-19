from pydantic import BaseModel

class LLMResponse(BaseModel):
    """
    Normalized response returned from any LLM provider
    """
    
    text : str 
    model : str
    