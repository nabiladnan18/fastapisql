"""add user table

Revision ID: fd3f4bb6b38e
Revises: cec55cdb6116
Create Date: 2023-11-26 03:05:19.141541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd3f4bb6b38e'
down_revision: Union[str, None] = 'cec55cdb6116'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')
