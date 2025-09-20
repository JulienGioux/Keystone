"""Add token to invitations and update user

Revision ID: bfb2f48b0265
Revises: 82689c25b22f
Create Date: 2025-09-20 14:54:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfb2f48b0265'
down_revision = '82689c25b22f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invitations', sa.Column('token', sa.String(), nullable=False))
    op.create_index(op.f('ix_invitations_token'), 'invitations', ['token'], unique=True)
    op.drop_column('users', 'hashed_password')


def downgrade():
    op.add_column('users', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_invitations_token'), table_name='invitations')
    op.drop_column('invitations', 'token')
