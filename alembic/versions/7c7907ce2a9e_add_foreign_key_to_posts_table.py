"""add foreign key to posts table

Revision ID: 7c7907ce2a9e
Revises: fd3f4bb6b38e
Create Date: 2023-11-26 03:43:06.327632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c7907ce2a9e'
down_revision: Union[str, None] = 'fd3f4bb6b38e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
