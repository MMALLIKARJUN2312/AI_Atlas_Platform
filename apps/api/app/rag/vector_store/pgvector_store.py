from __future__ import annotations

from sqlalchemy import select, delete
from sqlalchemy.orm import Session 

from app.database.models.embedding import Embedding
from app.rag.schemas.embedded_chunk import EmbeddedChunk

class PGVectorStore:
    """
    PostgreSQL + pgvector storage engine
    Responsible only for persistence and vector search
    """
    
    def __init__(self, db : Session):
        self.db = db
        
    def insert(self, chunk : EmbeddedChunk) -> Embedding:
        record = Embedding(
            document_id=chunk.chunk.document_id,
            chunk_id=chunk.chunk.chunk_id,
            document_type=chunk.chunk.metadata.get("document_type", ""),
            chunk_index=chunk.chunk.chunk_index,
            content=chunk.chunk.text,
            chunk_metadata=chunk.chunk.metadata,
            embedding=chunk.embedding,
            embedding_model=chunk.model,
            embedding_dimensions=chunk.dimensions
        )
        
        self.db.add(record)
        self.db.commit()                                                                                    
        self.db.refresh(record)
        
        return record

    def bulk_insert(self, chunks : list[EmbeddedChunk]) -> None:
        records = [
            Embedding(
                document_id=chunk.chunk.document_id,
                chunk_id=chunk.chunk.chunk_id,
                document_type=chunk.chunk.metadata.get("document_type", ""),
                chunk_index=chunk.chunk.chunk_index,
                content=chunk.chunk.text,
                chunk_metadata=chunk.chunk.metadata,
                embedding=chunk.embedding,
                embedding_model=chunk.model,
                embedding_dimensions=chunk.dimensions
            )
            for chunk in chunks
        ]
        
        self.db.add_all(records)
        self.db.commit()
            
    def get_document_chunks(self, document_id : str) -> list[Embedding]:
        return list(self.db.scalars(select(Embedding).where(Embedding.document_id == document_id).order_by(Embedding.chunk_index)))
    
    def similarity_search(self, embedding : list[float], top_k : int = 10) -> list[Embedding]:
        statement = (select(Embedding).order_by(Embedding.embedding.cosine_distance(embedding)).limit(top_k))
        
        return list(self.db.scalars(statement))
    
    def delete_document(self, document_id : str) -> None:
        self.db.execute(delete(Embedding).where(Embedding.document_id == document_id))
        
        self.db.commit()
        
    def reindex_document(self, chunks : list[EmbeddedChunk]) -> None:
        if not chunks:
            return
        
        document_id = chunks[0].chunk.document_id
        self.delete_document(document_id)
        self.bulk_insert(chunks)