from pydantic import BaseModel

class RetrievalResult(BaseModel):
    """
    Single retrieved chunk
    """
    
    document_id : str
    chunk_id : str
    document_type : str
    chunk_index : int 
    content : str 
    metadata : dict
    similarity_score : float
    