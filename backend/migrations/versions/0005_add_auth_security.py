"""add auth security fields

Revision ID: 0005_add_auth_security
Revises: 0004_add_auth_sessions
Create Date: 2026-08-08
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_add_auth_security"
down_revision = "0004_add_auth_sessions"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "locked_until",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("users", "locked_until")
    op.drop_column("users", "failed_login_attempts")
