from dataclasses import dataclass
from app.rag.vector_store.vector_config import VectorConfig

@dataclass(frozen=True)
class EmbeddingConfig:
    provider : str 
    model : str 
    dimensions: int = VectorConfig.EMBEDDING_DIMENSIONS
    batch_size : int = 32