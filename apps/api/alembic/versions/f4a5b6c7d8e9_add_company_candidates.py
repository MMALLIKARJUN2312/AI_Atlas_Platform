"""add company discovery candidates

Revision ID: f4a5b6c7d8e9
Revises: 982e11f65567
"""
from alembic import op
import sqlalchemy as sa

revision = "f4a5b6c7d8e9"
down_revision = "982e11f65567"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "company_candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("category", sa.Text(), nullable=False),
        sa.Column("segment_tags", sa.Text(), nullable=False),
        sa.Column("use_cases", sa.Text(), nullable=False),
        sa.Column("website", sa.String(length=255), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_company_candidates_name", "company_candidates", ["name"])
    op.create_index("ix_company_candidates_status", "company_candidates", ["status"])


def downgrade() -> None:
    op.drop_index("ix_company_candidates_status", table_name="company_candidates")
    op.drop_index("ix_company_candidates_name", table_name="company_candidates")
    op.drop_table("company_candidates")
