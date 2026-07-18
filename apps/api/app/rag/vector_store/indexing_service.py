from __future__ import annotations

from app.rag.chunkers.base_chunker import BaseChunker
from app.rag.embedders.base_embedder import BaseEmbedder
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.vector_store.pgvector_store import PGVectorStore

class IndexingService:
    """
    Central Indexing pipeline
    Every knowledge producer (CSV, News, Admin, AI Discovery uses this service)
    """
    
    def __init__(self, chunker : BaseChunker, embedder : BaseEmbedder, vector_store : PGVectorStore):
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        
    def index_document(self, document : KnowledgeDocument) -> None:
        chunks = self.chunker.chunk(document)
        embedded_chunks = self.embedder.embed(chunks)
        self.vector_store.reindex_document(embedded_chunks)
        
    def index_documents(self, documents : list[KnowledgeDocument]) -> None:
        for document in documents:
            self.index_document(document)
        
    