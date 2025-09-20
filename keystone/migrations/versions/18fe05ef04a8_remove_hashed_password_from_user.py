"""Remove hashed_password from user

Revision ID: 18fe05ef04a8
Revises: aaf95f372593
Create Date: 2025-09-20 13:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18fe05ef04a8'
down_revision = 'aaf95f372593'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'hashed_password')


def downgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
