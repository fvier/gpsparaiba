"""add financial subcategories

Revision ID: d6f704253647
Revises: c5e6f7031425
Create Date: 2026-08-03 17:20:00
"""
from alembic import op
import sqlalchemy as sa


revision = 'd6f704253647'
down_revision = 'c5e6f7031425'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('financial_categories', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_financial_category_parent', 'financial_categories',
                          'financial_categories', ['parent_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_financial_category_parent', 'financial_categories', type_='foreignkey')
    op.drop_column('financial_categories', 'parent_id')
