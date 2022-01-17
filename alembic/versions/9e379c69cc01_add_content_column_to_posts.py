"""add content column to posts

Revision ID: 9e379c69cc01
Revises: b090969ea1ef
Create Date: 2022-01-17 13:30:38.876435

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9e379c69cc01"
down_revision = "b090969ea1ef"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
