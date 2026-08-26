"""Add MetaTrader account fields to trading_accounts

Revision ID: 0010_add_mt5_accounts
Revises: 0009_challenge_daily_baseline
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0010_add_mt5_accounts"
down_revision: Union[str, Sequence[str], None] = "0009_challenge_daily_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "trading_accounts",
        sa.Column(
            "platform", sa.String(length=20), nullable=False, server_default="MT5"
        ),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("server", sa.String(length=120), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("login", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column(
            "account_kind", sa.String(length=10), nullable=False, server_default="DEMO"
        ),
    )
    op.add_column(
        "trading_accounts",
        sa.Column(
            "status", sa.String(length=20), nullable=False, server_default="PENDING"
        ),
    )
    op.add_column(
        "trading_accounts",
        sa.Column(
            "is_default", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )
    op.add_column(
        "trading_accounts",
        sa.Column(
            "equity", sa.Numeric(20, 8), nullable=False, server_default="0"
        ),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("leverage", sa.Integer(), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("credential_ref", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("last_connected_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column("last_error", sa.Text(), nullable=True),
    )
    op.add_column(
        "trading_accounts",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uq_trading_accounts_user_platform_server_login",
        "trading_accounts",
        ["user_id", "platform", "server", "login"],
    )
    op.create_index(
        "ix_trading_accounts_user_status",
        "trading_accounts",
        ["user_id", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_trading_accounts_user_status", table_name="trading_accounts")
    op.drop_constraint(
        "uq_trading_accounts_user_platform_server_login",
        "trading_accounts",
        type_="unique",
    )

    for column in (
        "updated_at",
        "last_error",
        "last_connected_at",
        "credential_ref",
        "leverage",
        "equity",
        "is_default",
        "status",
        "account_kind",
        "login",
        "server",
        "platform",
    ):
        op.drop_column("trading_accounts", column)
