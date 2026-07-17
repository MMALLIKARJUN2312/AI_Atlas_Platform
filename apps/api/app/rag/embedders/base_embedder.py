from __future__ import annotations

from abc import ABC, abstractmethod

from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.embedded_chunk import EmbeddedChunk

class BaseEmbedder(ABC):
    
    @abstractmethod
    def embed(self, chunks : list[KnowledgeChunk]) -> list[EmbeddedChunk]:
        """
        Generate Embeddings for knowledge chunks
        """
        raise NotImplementedError
        