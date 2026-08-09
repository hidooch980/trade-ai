"""add SaaS subscription and entitlement core

Revision ID: 0007_add_saas_core
Revises: d381dbfe0f51
Create Date: 2026-08-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0007_add_saas_core"
down_revision: Union[str, Sequence[str], None] = "d381dbfe0f51"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # subscription_plans
    # ---------------------------------------------------------
    op.create_table(
        "subscription_plans",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "price",
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
            "billing_cycle",
            sa.String(20),
            nullable=False,
            server_default="monthly",
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
            name="uq_subscription_plans_code",
        ),
    )

    # ---------------------------------------------------------
    # entitlements
    # ---------------------------------------------------------
    op.create_table(
        "entitlements",
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
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "code",
            name="uq_entitlements_code",
        ),
    )

    # ---------------------------------------------------------
    # plan_entitlements
    # ---------------------------------------------------------
    op.create_table(
        "plan_entitlements",
        sa.Column(
            "plan_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "entitlement_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["subscription_plans.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["entitlement_id"],
            ["entitlements.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "plan_id",
            "entitlement_id",
        ),
    )

    # ---------------------------------------------------------
    # subscriptions
    # ---------------------------------------------------------
    op.create_table(
        "subscriptions",
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
            "status",
            sa.String(20),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "starts_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "ends_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "auto_renew",
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["subscription_plans.id"],
            ondelete="RESTRICT",
        ),
    )

    op.create_index(
        "ix_subscriptions_user_id",
        "subscriptions",
        ["user_id"],
    )

    op.create_index(
        "ix_subscriptions_status",
        "subscriptions",
        ["status"],
    )

    # ---------------------------------------------------------
    # user_usage
    # ---------------------------------------------------------
    op.create_table(
        "user_usage",
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
            "period_start",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "period_end",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "signals_used",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "trades_used",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "api_calls_used",
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
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "user_id",
            "period_start",
            "period_end",
            name="uq_user_usage_period",
        ),
    )

    op.create_index(
        "ix_user_usage_user_id",
        "user_usage",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_user_usage_user_id",
        table_name="user_usage",
    )

    op.drop_table("user_usage")

    op.drop_index(
        "ix_subscriptions_status",
        table_name="subscriptions",
    )

    op.drop_index(
        "ix_subscriptions_user_id",
        table_name="subscriptions",
    )

    op.drop_table("subscriptions")

    op.drop_table("plan_entitlements")
    op.drop_table("entitlements")
    op.drop_table("subscription_plans")
