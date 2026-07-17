from app.rag.embedders.base_embedder import BaseEmbedder
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.gemini_embedder import GeminiEmbedder

class EmbedderFactory:
    
    @staticmethod
    def create(config : EmbeddingConfig) -> BaseEmbedder:
        
        if config.provider == "gemini":
            return GeminiEmbedder(config)
        
        raise ValueError(f"Unsupported embedding provider : {config.provider}")