"""create_projects_table

Revision ID: e6b3470e27a1
Revises: 
Create Date: 2022-11-07 08:40:57.871738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'e6b3470e27a1'
down_revision = None
branch_labels = None
depends_on = None


def create_projects_table() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(15), nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True, index=True),
        sa.Column('image', sa.String, nullable=True)
    )


def upgrade() -> None:
    create_projects_table()


def downgrade() -> None:
    op.drop_table("projects")

