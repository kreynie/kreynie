"""initial

Revision ID: 77cc4fb5103c
Revises: 
Create Date: 2023-11-20 01:26:55.720480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77cc4fb5103c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "hot_issues",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("published", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("hot_issues", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_hot_issues_published"), ["published"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_hot_issues_title"), ["title"], unique=False
        )

    op.create_table(
        "stuff_groups",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stuffs",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.Integer(), nullable=False),
        sa.Column("allowance", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["stuff_groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "group_id", "key", name="uix_stuff_account"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stuffs")
    op.drop_table("users")
    op.drop_table("stuff_groups")
    with op.batch_alter_table("hot_issues", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_hot_issues_title"))
        batch_op.drop_index(batch_op.f("ix_hot_issues_published"))

    op.drop_table("hot_issues")
    # ### end Alembic commands ###
