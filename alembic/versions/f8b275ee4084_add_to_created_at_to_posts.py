"""add to created_at to posts

Revision ID: f8b275ee4084
Revises: a592a70d4378
Create Date: 2022-01-17 14:01:20.456300

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f8b275ee4084"
down_revision = "a592a70d4378"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
