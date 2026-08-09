"""add challenge daily baseline

Revision ID: 0009_add_challenge_daily_baseline
Revises: 0008_add_challenge_core
Create Date: 2026-08-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0009_add_challenge_daily_baseline"
down_revision: Union[str, Sequence[str], None] = "0008_add_challenge_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "challenge_metrics",
        sa.Column(
            "day_start_equity",
            sa.Numeric(14, 2),
            nullable=False,
            server_default="0",
        ),
    )

    op.create_index(
        "ix_challenge_metrics_trading_date",
        "challenge_metrics",
        ["trading_date"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_challenge_metrics_trading_date",
        table_name="challenge_metrics",
    )

    op.drop_column(
        "challenge_metrics",
        "day_start_equity",
    )
