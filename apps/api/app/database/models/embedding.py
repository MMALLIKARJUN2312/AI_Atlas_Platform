from __future__ import annotations

from datetime import datetime

from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.rag.vector_store.vector_config import VectorConfig

class Embedding(Base):
    """
    Stores every embedded chunk inside PostgreSQL.
    This table is the central knowledge index used by : 
    Ask AI, Semantic Search, Hybrid Search, News Retrieval, Company Discovery
    """
    
    __tablename__ = "embeddings"
    
    id : Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda : str(uuid4()))
    document_id : Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    chunk_id : Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    document_type : Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    chunk_index : Mapped[int] = mapped_column(Integer, nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    chunk_metadata : Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)
    embedding : Mapped[list[float]] = mapped_column(Vector(VectorConfig.EMBEDDING_DIMENSIONS), nullable=False)
    embedding_model : Mapped[str] = mapped_column(String(100), nullable=False)
    embedding_dimensions : Mapped[int] = mapped_column(Integer, nullable=False)
    search_vector : Mapped[str] = mapped_column(TSVECTOR, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (Index("ix_embeddings_document_chunk", "document_id", "chunk_index"),)