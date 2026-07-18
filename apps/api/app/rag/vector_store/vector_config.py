from dataclasses import dataclass

@dataclass(frozen=True)
class VectorConfig:
    """
    Global configuration for the vector store file.
    """
    
    EMBEDDING_MODEL : str = "gemini-embedding-001"
    EMBEDDING_DIMENSIONS : int = 768
    DEFAULT_TOP_K : int = 10
    DISTANCE_METRIC : str = "cosine"
    INDEX_NAME : str = "idx_embeddings_hnsw"
    
    HNSW_M : int = 16
    HNSW_EF_CONSTRUCTION : int = 64