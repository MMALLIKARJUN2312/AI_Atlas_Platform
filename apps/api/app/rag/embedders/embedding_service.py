from __future__ import annotations

from app.rag.embedders.gemini_embedder import GeminiEmbedder
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.embedded_chunk import EmbeddedChunk
from app.rag.embedders.base_embedder import BaseEmbedder
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.embedder_factory import EmbedderFactory

class EmbeddingService:
    
    def __init__(self, embedder : BaseEmbedder):
        self.embedder = embedder
        
    def generate(self, chunks : list[KnowledgeChunk]) -> list[EmbeddedChunk]:
        return self.embedder.embed(chunks)
    
    def embed_query(self, query: str) -> list[float]:
        return self.embedder.embed_query(query)