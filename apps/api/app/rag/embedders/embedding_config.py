from dataclasses import dataclass

@dataclass(frozen=True)
class EmbeddingConfig:
    provider : str 
    model : str 
    batch_size : int = 32