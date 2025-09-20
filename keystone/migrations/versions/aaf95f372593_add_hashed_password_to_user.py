"""Add hashed_password to user

Revision ID: aaf95f372593
Revises: 067c920e7b56
Create Date: 2025-09-20 13:08:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf95f372593'
down_revision = '067c920e7b56'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))


def downgrade():
    op.drop_column('users', 'hashed_password')
