"""create posts table

Revision ID: c24058f693f6
Revises: 
Create Date: 2023-11-26 01:54:23.116248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c24058f693f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(),
                  nullable=False, primary_key=True),
        sa.Column('title', sa.String(),
                  nullable=False, unique=True),
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
