from pydantic import BaseModel
from app.rag.retrievers.retrieval_result import RetrievalResult

class RetrievalOutput(BaseModel):
    """
    Output returned by the retrieval pipeline
    """
    
    context : str 
    results : list[RetrievalResult]
    