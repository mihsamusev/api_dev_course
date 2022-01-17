"""create post table

Revision ID: b090969ea1ef
Revises: 
Create Date: 2022-01-17 13:19:28.644426

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b090969ea1ef"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
