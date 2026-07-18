from pydantic import BaseModel

class Citation(BaseModel):
    """
    Source citation for retrieved context
    """
    
    document_id : str 
    chunk_id : str 
    document_type : str 
    