"""add new columns to posts

Revision ID: cec55cdb6116
Revises: c24058f693f6
Create Date: 2023-11-26 02:28:06.342833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cec55cdb6116'
down_revision: Union[str, None] = 'c24058f693f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'title')
