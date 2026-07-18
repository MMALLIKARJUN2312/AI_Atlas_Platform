from pydantic import BaseModel

from app.ai.schemas.citation import Citation

class AskAIResponse(BaseModel):
    """
    Final response returned to the frontend
    """
    
    answer : str 
    citations : list[Citation]
    
    
    