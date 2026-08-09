"""add challenge core

Revision ID: 0008_add_challenge_core
Revises: 0007_add_saas_core
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0008_add_challenge_core"
down_revision: Union[str, Sequence[str], None] = "0007_add_saas_core"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # challenge_plans
    # ---------------------------------------------------------
    op.create_table(
        "challenge_plans",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),

        sa.Column(
            "starting_balance",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "challenge_fee",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "currency",
            sa.String(3),
            nullable=False,
            server_default="EUR",
        ),

        sa.Column(
            "profit_target_percent",
            sa.Numeric(6, 3),
            nullable=False,
        ),

        sa.Column(
            "daily_drawdown_percent",
            sa.Numeric(6, 3),
            nullable=False,
        ),

        sa.Column(
            "max_drawdown_percent",
            sa.Numeric(6, 3),
            nullable=False,
        ),

        sa.Column(
            "min_trading_days",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "max_trading_days",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "code",
            name="uq_challenge_plans_code",
        ),
    )

    # ---------------------------------------------------------
    # challenge_accounts
    # ---------------------------------------------------------
    op.create_table(
        "challenge_accounts",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "plan_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "account_number",
            sa.String(50),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="ACTIVE",
        ),

        sa.Column(
            "initial_balance",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "balance",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "equity",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "peak_equity",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "failed_reason",
            sa.String(255),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["challenge_plans.id"],
            ondelete="RESTRICT",
        ),

        sa.UniqueConstraint(
            "account_number",
            name="uq_challenge_accounts_account_number",
        ),
    )

    op.create_index(
        "ix_challenge_accounts_user_id",
        "challenge_accounts",
        ["user_id"],
    )

    op.create_index(
        "ix_challenge_accounts_status",
        "challenge_accounts",
        ["status"],
    )

    # ---------------------------------------------------------
    # challenge_metrics
    # ---------------------------------------------------------
    op.create_table(
        "challenge_metrics",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "challenge_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "trading_date",
            sa.Date(),
            nullable=False,
        ),

        sa.Column(
            "balance",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "equity",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "daily_profit",
            sa.Numeric(14, 2),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "daily_drawdown_percent",
            sa.Numeric(8, 4),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "total_profit_percent",
            sa.Numeric(8, 4),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "max_drawdown_percent",
            sa.Numeric(8, 4),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "trades_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["challenge_account_id"],
            ["challenge_accounts.id"],
            ondelete="CASCADE",
        ),

        sa.UniqueConstraint(
            "challenge_account_id",
            "trading_date",
            name="uq_challenge_metrics_day",
        ),
    )

    op.create_index(
        "ix_challenge_metrics_account_id",
        "challenge_metrics",
        ["challenge_account_id"],
    )

    # ---------------------------------------------------------
    # challenge_events
    # ---------------------------------------------------------
    op.create_table(
        "challenge_events",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "challenge_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "event_type",
            sa.String(50),
            nullable=False,
        ),

        sa.Column(
            "event_data",
            postgresql.JSONB(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["challenge_account_id"],
            ["challenge_accounts.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_challenge_events_account_id",
        "challenge_events",
        ["challenge_account_id"],
    )

    op.create_index(
        "ix_challenge_events_type",
        "challenge_events",
        ["event_type"],
    )

    # ---------------------------------------------------------
    # challenge_results
    # ---------------------------------------------------------
    op.create_table(
        "challenge_results",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "challenge_account_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "result",
            sa.String(20),
            nullable=False,
        ),

        sa.Column(
            "profit_target_reached",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),

        sa.Column(
            "daily_drawdown_ok",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "max_drawdown_ok",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "minimum_trading_days_ok",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),

        sa.Column(
            "rules_ok",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "final_balance",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "final_equity",
            sa.Numeric(14, 2),
            nullable=False,
        ),

        sa.Column(
            "final_profit_percent",
            sa.Numeric(8, 4),
            nullable=False,
        ),

        sa.Column(
            "reason",
            sa.String(255),
            nullable=True,
        ),

        sa.Column(
            "evaluated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["challenge_account_id"],
            ["challenge_accounts.id"],
            ondelete="CASCADE",
        ),

        sa.UniqueConstraint(
            "challenge_account_id",
            name="uq_challenge_results_account",
        ),
    )


def downgrade() -> None:

    op.drop_table("challenge_results")

    op.drop_index(
        "ix_challenge_events_type",
        table_name="challenge_events",
    )

    op.drop_index(
        "ix_challenge_events_account_id",
        table_name="challenge_events",
    )

    op.drop_table("challenge_events")

    op.drop_index(
        "ix_challenge_metrics_account_id",
        table_name="challenge_metrics",
    )

    op.drop_table("challenge_metrics")

    op.drop_index(
        "ix_challenge_accounts_status",
        table_name="challenge_accounts",
    )

    op.drop_index(
        "ix_challenge_accounts_user_id",
        table_name="challenge_accounts",
    )

    op.drop_table("challenge_accounts")

    op.drop_table("challenge_plans")
