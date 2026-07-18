"""create embeddings table

Revision ID: 862b05f714bc
Revises: 2bf3d401cb71
Create Date: 2026-07-18 03:19:01.860513
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB

from app.rag.vector_store.vector_config import VectorConfig


# revision identifiers, used by Alembic.
revision: str = "862b05f714bc"
down_revision: Union[str, Sequence[str], None] = "2bf3d401cb71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "embeddings",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("document_id", sa.String(length=255), nullable=False),
        sa.Column("chunk_id", sa.String(length=255), nullable=False, unique=True),
        sa.Column("document_type", sa.String(length=50), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", JSONB, nullable=False),
        sa.Column(
            "embedding",
            Vector(VectorConfig.EMBEDDING_DIMENSIONS),
            nullable=False,
        ),
        sa.Column("embedding_model", sa.String(length=100), nullable=False),
        sa.Column("embedding_dimensions", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_embeddings_document_id",
        "embeddings",
        ["document_id"],
    )

    op.create_index(
        "ix_embeddings_chunk_id",
        "embeddings",
        ["chunk_id"],
    )

    op.create_index(
        "ix_embeddings_document_type",
        "embeddings",
        ["document_type"],
    )

    op.create_index(
        "ix_embeddings_document_chunk",
        "embeddings",
        ["document_id", "chunk_index"],
    )

    op.execute(
        f"""
        CREATE INDEX {VectorConfig.INDEX_NAME}
        ON embeddings
        USING hnsw (
            embedding vector_cosine_ops
        )
        WITH (
            m = {VectorConfig.HNSW_M},
            ef_construction = {VectorConfig.HNSW_EF_CONSTRUCTION}
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.execute(
        f"DROP INDEX IF EXISTS {VectorConfig.INDEX_NAME};"
    )

    op.drop_index(
        "ix_embeddings_document_chunk",
        table_name="embeddings",
    )

    op.drop_index(
        "ix_embeddings_document_type",
        table_name="embeddings",
    )

    op.drop_index(
        "ix_embeddings_chunk_id",
        table_name="embeddings",
    )

    op.drop_index(
        "ix_embeddings_document_id",
        table_name="embeddings",
    )

    op.drop_table("embeddings")