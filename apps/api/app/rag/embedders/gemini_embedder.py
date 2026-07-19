from __future__ import annotations

from google import genai
from google.genai import types

from app.core.config import settings
from app.rag.embedders.base_embedder import BaseEmbedder
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.embedded_chunk import EmbeddedChunk

class GeminiEmbedder(BaseEmbedder):
    
    def __init__(self, config : EmbeddingConfig):
        self.client = genai.Client(api_key=settings.LLM_API_KEY)
        self.config = config
        
    def embed(self, chunks : list[KnowledgeChunk]) -> list[EmbeddedChunk]:
        results : list[EmbeddedChunk] = []
        
        for chunk in chunks:
            response = self.client.models.embed_content(
            model=self.config.model,
            contents=chunk.text,
            config=types.EmbedContentConfig(
                output_dimensionality=self.config.dimensions
                ),
            )
            
            vector = response.embeddings[0].values
            
            results.append(
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=vector,
                    model=self.config.model,
                    dimensions=len(vector)
                )
            )
            
        return results
    
    def embed_query(self, query: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.config.model,
            contents=query,
            config=types.EmbedContentConfig(
                output_dimensionality=self.config.dimensions
            ),
        )

        return response.embeddings[0].values