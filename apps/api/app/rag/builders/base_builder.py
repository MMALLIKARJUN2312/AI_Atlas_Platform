from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar 

from app.rag.schemas.knowledge_document import KnowledgeDocument

ModelType = TypeVar("ModelType")

class BaseDocumentBuilder(ABC, Generic[ModelType]):
    """
    Converts ORM models into canonical KnowledgeDocuments.
    """
    
    @abstractmethod
    def build(self, entity : ModelType) -> KnowledgeDocument:
        """
        Transform one ORM entity into a KnowledgeDocument
        """
        
        raise NotImplementedError
        
    
