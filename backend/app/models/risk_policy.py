from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AccountRiskPolicy(Base):
    """
    One account's risk limits, plus the two references the daily and total
    rules measure against.

    Limits and running state live together because they are read together on
    every assessment and are meaningless apart; the state columns are named
    so it stays obvious which is which.
    """

    __tablename__ = "account_risk_policies"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    account_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("trading_accounts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # ---- limits ----------------------------------------------------------

    max_daily_loss_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3), nullable=False, default=Decimal("5"), server_default="5"
    )
    max_total_loss_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3), nullable=False, default=Decimal("10"), server_default="10"
    )
    max_risk_per_trade_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3), nullable=False, default=Decimal("1"), server_default="1"
    )
    max_open_positions: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5, server_default="5"
    )
    max_total_exposure_ratio: Mapped[Decimal] = mapped_column(
        Numeric(8, 3), nullable=False, default=Decimal("10"), server_default="10"
    )
    max_symbol_exposure_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3), nullable=False, default=Decimal("50"), server_default="50"
    )
    max_correlated_positions: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3, server_default="3"
    )
    warn_at_percent: Mapped[Decimal] = mapped_column(
        Numeric(6, 3), nullable=False, default=Decimal("80"), server_default="80"
    )

    # ---- state the rules measure against ---------------------------------

    #: Equity when the trading day was last reset.
    day_start_equity: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 8), nullable=True
    )
    day_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    #: Highest equity ever recorded on this account.
    peak_equity: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 8), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
