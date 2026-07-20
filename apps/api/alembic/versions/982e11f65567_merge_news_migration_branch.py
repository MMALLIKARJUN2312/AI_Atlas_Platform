"""merge news migration branch

Revision ID: 982e11f65567
Revises: 691a3db1a542, c8e1d3f4a5b6
Create Date: 2026-07-20 08:05:10.783800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '982e11f65567'
down_revision: Union[str, Sequence[str], None] = ('691a3db1a542', 'c8e1d3f4a5b6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
