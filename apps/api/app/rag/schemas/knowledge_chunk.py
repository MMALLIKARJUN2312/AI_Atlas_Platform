from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

class KnowledgeChunk(BaseModel):
    """
    Represents one semantic chunk generated from a Knowledge Document.
    """
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    chunk_id : str
    document_id : str
    chunk_index : int
    text : str
    metadata : dict[str, Any]
    