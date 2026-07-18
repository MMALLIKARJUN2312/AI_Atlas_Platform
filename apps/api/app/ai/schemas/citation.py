from pydantic import BaseModel

class Citation(BaseModel):
    """
    Citation received for an AI answer
    """
    
    document_id : str 
    chunk_id : str
    document_type : str 