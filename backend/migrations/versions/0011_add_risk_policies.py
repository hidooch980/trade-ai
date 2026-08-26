"""Add per-account risk policies

Revision ID: 0011_add_risk_policies
Revises: 0010_add_mt5_accounts
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0011_add_risk_policies"
down_revision: Union[str, Sequence[str], None] = "0010_add_mt5_accounts"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "account_risk_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "max_daily_loss_percent", sa.Numeric(6, 3), nullable=False, server_default="5"
        ),
        sa.Column(
            "max_total_loss_percent", sa.Numeric(6, 3), nullable=False, server_default="10"
        ),
        sa.Column(
            "max_risk_per_trade_percent",
            sa.Numeric(6, 3),
            nullable=False,
            server_default="1",
        ),
        sa.Column("max_open_positions", sa.Integer(), nullable=False, server_default="5"),
        sa.Column(
            "max_total_exposure_ratio",
            sa.Numeric(8, 3),
            nullable=False,
            server_default="10",
        ),
        sa.Column(
            "max_symbol_exposure_percent",
            sa.Numeric(6, 3),
            nullable=False,
            server_default="50",
        ),
        sa.Column(
            "max_correlated_positions", sa.Integer(), nullable=False, server_default="3"
        ),
        sa.Column("warn_at_percent", sa.Numeric(6, 3), nullable=False, server_default="80"),
        sa.Column("day_start_equity", sa.Numeric(20, 8), nullable=True),
        sa.Column("day_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("peak_equity", sa.Numeric(20, 8), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["account_id"], ["trading_accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_id", name="uq_account_risk_policies_account_id"),
    )


def downgrade() -> None:
    op.drop_table("account_risk_policies")
