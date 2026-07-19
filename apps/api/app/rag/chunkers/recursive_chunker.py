from __future__ import annotations

import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.chunkers.base_chunker import BaseChunker
from app.rag.chunkers.chunking_config import ChunkingConfig
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.knowledge_document import KnowledgeDocument

class RecursiveChunker(BaseChunker):

    def __init__(self, config : ChunkingConfig | None = None):
        self.config = config or ChunkingConfig()
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.config.chunk_size,
            chunk_overlap = self.config.chunk_overlap,
            separators = list(self.config.separators)
        )
        
    def chunk(self, document : KnowledgeDocument) -> list[KnowledgeChunk]:
        pieces = self.splitter.split_text(document.content)
        chunks : list[KnowledgeChunk] = []
        
        for index, text in enumerate(pieces):
            chunks.append(KnowledgeChunk(
                chunk_id=str(uuid.uuid4()),
                document_id = document.document_id,
                document_type=document.document_type,
                chunk_index = index,
                text = text,
                metadata = document.metadata
            ))
            
        return chunks