from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ChallengeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PASSED = "PASSED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class ChallengeResultStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"


class ChallengePlan(Base):
    __tablename__ = "challenge_plans"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    starting_balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    challenge_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        server_default="0",
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="EUR",
        server_default="EUR",
    )

    profit_target_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3),
        nullable=False,
    )

    daily_drawdown_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3),
        nullable=False,
    )

    max_drawdown_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3),
        nullable=False,
    )

    min_trading_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    max_trading_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=func.true(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class ChallengeAccount(Base):
    __tablename__ = "challenge_accounts"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    plan_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("challenge_plans.id", ondelete="RESTRICT"),
        nullable=False,
    )

    account_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ChallengeStatus.ACTIVE.value,
        server_default="ACTIVE",
        index=True,
    )

    initial_balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    equity: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    peak_equity: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    failed_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )


class ChallengeMetric(Base):
    __tablename__ = "challenge_metrics"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    challenge_account_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("challenge_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    trading_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    equity: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    day_start_equity: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
        server_default="0",
    )

    daily_profit: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
        server_default="0",
    )

    daily_drawdown_percent: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        default=0,
        server_default="0",
    )

    total_profit_percent: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        default=0,
        server_default="0",
    )

    max_drawdown_percent: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        default=0,
        server_default="0",
    )

    trades_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "challenge_account_id",
            "trading_date",
            name="uq_challenge_metrics_day",
        ),
    )


class ChallengeEvent(Base):
    __tablename__ = "challenge_events"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    challenge_account_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("challenge_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    event_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class ChallengeResult(Base):
    __tablename__ = "challenge_results"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    challenge_account_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("challenge_accounts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    profit_target_reached: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=func.false(),
    )

    daily_drawdown_ok: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=func.true(),
    )

    max_drawdown_ok: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=func.true(),
    )

    minimum_trading_days_ok: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=func.false(),
    )

    rules_ok: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=func.true(),
    )

    final_balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    final_equity: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    final_profit_percent: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
