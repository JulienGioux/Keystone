"""Remove hashed_password from user

Revision ID: 48a4f98a6ec3
Revises: 82689c25b22f
Create Date: 2025-09-20 16:13:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48a4f98a6ec3'
down_revision = '82689c25b22f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'hashed_password')


def downgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
