from pydantic import BaseModel, Field

class AskAIRequest(BaseModel):
    """
    User question
    """
    
    question : str = Field(..., min_length=3, max_length=1000)
    
    