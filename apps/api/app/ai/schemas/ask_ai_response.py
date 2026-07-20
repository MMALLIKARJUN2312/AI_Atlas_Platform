from pydantic import BaseModel

from app.ai.schemas.citation import Source

class AskAIResponse(BaseModel):
    """
    Final response returned to the frontend
    """
    
    answer : str 
    sources: list[Source]
    
