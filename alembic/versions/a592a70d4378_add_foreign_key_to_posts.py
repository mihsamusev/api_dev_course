"""add foreign key to posts

Revision ID: a592a70d4378
Revises: cd56c3130e07
Create Date: 2022-01-17 13:49:13.328800

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a592a70d4378"
down_revision = "cd56c3130e07"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="post")
    op.drop_column("posts", "owner_id")
