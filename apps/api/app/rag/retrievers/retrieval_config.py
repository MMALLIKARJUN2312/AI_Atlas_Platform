from dataclasses import dataclass 

@dataclass(frozen=True)
class RetrievalConfig:
    """
    Configuration for semantic retrieval
    """
    
    DEFAULT_TOP_K : int = 10
    MIN_SIMILARITY_SCORE : float = 0.60
    MAX_CONTENT_CHUNKS : int = 8
    