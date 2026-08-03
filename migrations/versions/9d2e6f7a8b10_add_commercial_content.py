"""add editable commercial plans and linktree

Revision ID: 9d2e6f7a8b10
Revises: 356ceaebf680
Create Date: 2026-08-03 10:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = '9d2e6f7a8b10'
down_revision = '356ceaebf680'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('commercial_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('vehicle_type', sa.String(length=80), nullable=False),
        sa.Column('coverage', sa.String(length=160), nullable=False),
        sa.Column('monthly_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('installation_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('description', sa.String(length=240), nullable=False),
        sa.Column('benefits', sa.Text(), nullable=False),
        sa.Column('badge', sa.String(length=60), nullable=False),
        sa.Column('whatsapp_url', sa.Text(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('featured', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'))
    op.create_table('linktree_links',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('subtitle', sa.String(length=180), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('icon', sa.String(length=60), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'))
    op.create_table('plan_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version_code', sa.String(length=32), nullable=False),
        sa.Column('snapshot', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('version_code'))


def downgrade():
    op.drop_table('plan_versions')
    op.drop_table('linktree_links')
    op.drop_table('commercial_plans')
