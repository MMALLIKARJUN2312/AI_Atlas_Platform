from __future__ import annotations

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.embedding import Embedding
from app.rag.schemas.embedded_chunk import EmbeddedChunk

class PGVectorStore:
    """
    PostgreSQL + pgvector storage engine
    Responsible only for persistence and vector search
    """
    
    def __init__(self, db : AsyncSession):
        self.db = db
        
    async def insert(self, chunk : EmbeddedChunk) -> Embedding:
        record = Embedding(
            document_id=chunk.chunk.document_id,
            document_type=chunk.chunk.document_type.value,
            chunk_id=chunk.chunk.chunk_id,
            chunk_index=chunk.chunk.chunk_index,
            content=chunk.chunk.text,
            chunk_metadata=chunk.chunk.metadata,
            embedding=chunk.embedding,
            embedding_model=chunk.model,
            embedding_dimensions=chunk.dimensions
        )
        
        self.db.add(record)
        await self.db.commit()                                                                                    
        await self.db.refresh(record)
        
        return record

    async def bulk_insert(self, chunks : list[EmbeddedChunk]) -> None:
        records = [
            Embedding(
                document_id=chunk.chunk.document_id,
                document_type=chunk.chunk.document_type.value,
                chunk_id=chunk.chunk.chunk_id,
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
        await self.db.commit()
            
    async def get_document_chunks(self, document_id : str) -> list[Embedding]:
        result = await self.db.scalars(select(Embedding).where(Embedding.document_id == document_id).order_by(Embedding.chunk_index))
        
        return list(result)    
    
    async def similarity_search(self, embedding : list[float], top_k : int = 10) -> list[tuple[Embedding, float]]:
        similarity = 1 - Embedding.embedding.cosine_distance(embedding)
        statement = (select(Embedding, similarity.label("score")).order_by(Embedding.embedding.cosine_distance(embedding)).limit(top_k))
        
        result = await self.db.execute(statement)
        
        return result.all()
    
    async def delete_document(self, document_id : str) -> None:
        await self.db.execute(delete(Embedding).where(Embedding.document_id == document_id))
        
        await self.db.commit()
        
    async def reindex_document(self, chunks : list[EmbeddedChunk]) -> None:
        if not chunks:
            return
        
        document_id = chunks[0].chunk.document_id
        await self.delete_document(document_id)
        await self.bulk_insert(chunks)