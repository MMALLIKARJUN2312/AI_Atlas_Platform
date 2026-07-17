from __future__ import annotations

from app.rag.embedders.gemini_embedder import GeminiEmbedder
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.embedded_chunk import EmbeddedChunk
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.embedder_factory import EmbedderFactory

class EmbeddingService:
    
    def __init__(self, config : EmbeddingConfig | None = None):
        self.config = config or EmbeddingConfig()
        self.embedder = EmbedderFactory.create(self.config)
        
    def generate(self, chunks : list[KnowledgeChunk]) -> list[EmbeddedChunk]:
        return self.embedder.embed(chunks)