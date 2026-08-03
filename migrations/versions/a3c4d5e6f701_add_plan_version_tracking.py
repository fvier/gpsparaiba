"""add individual plan version tracking

Revision ID: a3c4d5e6f701
Revises: 9d2e6f7a8b10
Create Date: 2026-08-03 16:10:00
"""
from alembic import op
import sqlalchemy as sa


revision = 'a3c4d5e6f701'
down_revision = '9d2e6f7a8b10'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('commercial_plans', sa.Column('last_version_code', sa.String(length=32), nullable=True))


def downgrade():
    op.drop_column('commercial_plans', 'last_version_code')
