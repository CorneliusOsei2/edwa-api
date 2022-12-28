"""create users table

Revision ID: 3ee3316ea547
Revises: 
Create Date: 2022-12-27 20:45:52.449482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3ee3316ea547"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "users", ["full_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "users", ["id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_user_id"), table_name="users")
    op.drop_index(op.f("ix_user_full_name"), table_name="users")
    op.drop_index(op.f("ix_user_email"), table_name="users")
    op.drop_table("users")
