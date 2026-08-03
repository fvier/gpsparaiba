"""add landing card assignments

Revision ID: b4d5e6f70213
Revises: a3c4d5e6f701
Create Date: 2026-08-03 16:30:00
"""
from alembic import op
import sqlalchemy as sa


revision = 'b4d5e6f70213'
down_revision = 'a3c4d5e6f701'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('landing_cards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slot', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('benefits', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['commercial_plans.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slot'))


def downgrade():
    op.drop_table('landing_cards')
