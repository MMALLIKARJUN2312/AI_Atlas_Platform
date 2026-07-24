"""fix search_vector not-null and restore hnsw index

Revision ID: b1c2d3e4f5a6
Revises: f4a5b6c7d8e9
Create Date: 2026-07-23 00:00:00.000000

A prior migration (691a3db1a542) added `search_vector` as NOT NULL with no
default and no application code populates it (the hybrid BM25 retriever that
would use it is built but not wired into the running app) - this made every
insert into `embeddings` fail with a NotNullViolation. The same migration
also dropped the HNSW vector index and never recreated it, degrading the
vector search that IS used in production. This migration fixes both without
touching the already-applied historical migration.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = 'f4a5b6c7d8e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('embeddings', 'search_vector', nullable=True)
    op.create_index(
        op.f('idx_embeddings_hnsw'),
        'embeddings',
        ['embedding'],
        unique=False,
        postgresql_using='hnsw',
        postgresql_with={'m': '16', 'ef_construction': '64'},
        postgresql_ops={'embedding': 'vector_cosine_ops'},
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_index(op.f('idx_embeddings_hnsw'), table_name='embeddings')
    op.alter_column('embeddings', 'search_vector', nullable=False)
