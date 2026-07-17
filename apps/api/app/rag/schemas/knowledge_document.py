from __future__ import annotations

from typing import Any
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.rag.schemas.document_type import DocumentType

class KnowledgeDocument(BaseModel):
    """
    Canonical document representation used throughout the RAG pipeline.
    
    Every datasource is transformed into this representation before chunking and embedding.
    """
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    document_id : str = Field(description="Globally unique document identifier.")
    document_type : DocumentType = Field(description="Document category (company, problem, mapping, sector, ...)") 
    source_id : int
    title : str 
    content : str 
    metadata : dict[str, Any]
    created_at : datetime
    updated_at : datetime
    