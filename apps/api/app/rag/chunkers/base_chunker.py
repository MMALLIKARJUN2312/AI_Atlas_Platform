from __future__ import annotations

from abc import ABC, abstractmethod

from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.knowledge_document import KnowledgeDocument

class BaseChunker(ABC):
    
    @abstractmethod
    def chunk(self, document : KnowledgeDocument) -> list[KnowledgeChunk]:
        """Split a document into semantic chunks"""
        raise NotImplementedError