from dataclasses import dataclass

@dataclass(frozen=True)
class ChunkingConfig:
    """
    Configuration for semantic text chunking.
    """
    
    chunk_size : int = 800
    chunk_overlap : int = 150
    separators : tuple[str, ...] = ("\n\n", "\n", ". ", "; ", " ")