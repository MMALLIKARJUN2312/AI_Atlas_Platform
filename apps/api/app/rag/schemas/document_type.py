from enum import StrEnum

class DocumentType(StrEnum):
    """
    Supported knowledge document types.
    These values are used throughout the RAG pipeline for indexing, retrieval, filtering and citations.
    """
    
    COMPANY = "company"
    PROBLEM = "problem"
    MAPPING = "mapping"
    SECTOR = "sector"
    NEWS = "news"