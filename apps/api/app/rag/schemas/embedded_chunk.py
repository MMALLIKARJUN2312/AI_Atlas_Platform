from __future__ import annotations

from pydantic import BaseModel

from app.rag.schemas.knowledge_chunk import KnowledgeChunk

class EmbeddedChunk(BaseModel):
    """
    Represents a knowledge chunk together with its embedding vector
    """
    
    chunk : KnowledgeChunk
    embedding : list[float]
    model : str 
    dimensions : int
    
    