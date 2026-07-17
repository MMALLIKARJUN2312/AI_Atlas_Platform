from dataclasses import dataclass

@dataclass(frozen=True)
class EmbeddingConfig:
    provider : str = "gemini"
    model : str = "gemini-embedding-001"
    batch_size : int = 32