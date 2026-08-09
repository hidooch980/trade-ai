"""add user language

Revision ID: 0003_add_user_language
Revises: 0002_add_user_password_hash
Create Date: 2026-08-08
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_add_user_language"
down_revision = "0002_add_user_password_hash"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "language",
            sa.String(length=10),
            nullable=False,
            server_default="en",
        ),
    )


def downgrade():
    op.drop_column("users", "language")
