"""add financial management

Revision ID: c5e6f7031425
Revises: b4d5e6f70213
Create Date: 2026-08-03 17:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = 'c5e6f7031425'
down_revision = 'b4d5e6f70213'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('financial_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('entry_type', sa.String(length=16), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'))
    op.create_table('financial_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entry_type', sa.String(length=16), nullable=False),
        sa.Column('description', sa.String(length=180), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=16), nullable=False),
        sa.Column('notes', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['financial_categories.id']),
        sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('financial_entries')
    op.drop_table('financial_categories')
