"""add published column to posts table

Revision ID: 9cec97a02cf1
Revises: 7c7907ce2a9e
Create Date: 2023-11-26 03:59:00.980004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cec97a02cf1'
down_revision: Union[str, None] = '7c7907ce2a9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),
                  nullable=False, server_default="True")
    )


def downgrade() -> None:
    op.drop_column(
        'posts',
        'published'
    )
