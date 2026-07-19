from __future__ import annotations

from app.rag.chunkers.base_chunker import BaseChunker
from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.vector_store.pgvector_store import PGVectorStore

class IndexingService:
    """
    Central Indexing pipeline
    Every knowledge producer (CSV, News, Admin, AI Discovery uses this service)
    """
    
    def __init__(self, chunker : BaseChunker, embedding_service : EmbeddingService, vector_store : PGVectorStore):
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        
    async def index_document(self, document : KnowledgeDocument) -> None:
        chunks = self.chunker.chunk(document)
        embedded_chunks = self.embedding_service.generate(chunks)
        await self.vector_store.reindex_document(embedded_chunks)
        
    async def index_documents(self, documents : list[KnowledgeDocument]) -> None:
        for document in documents:
            await self.index_document(document)
        
    