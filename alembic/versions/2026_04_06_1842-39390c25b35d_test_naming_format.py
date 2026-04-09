"""test_naming_format

Revision ID: 39390c25b35d
Revises: bc08fb91af22
Create Date: 2026-04-06 18:42:45.484468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39390c25b35d'
down_revision: Union[str, Sequence[str], None] = 'bc08fb91af22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
