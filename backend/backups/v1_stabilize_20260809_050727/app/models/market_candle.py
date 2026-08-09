from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class MarketCandle(Base):
    __tablename__ = "market_candles"

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "timeframe",
            "open_time",
            name="uq_market_candle_symbol_timeframe_open_time",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    symbol_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("symbols.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    timeframe: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    open_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    close_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    open: Mapped[Decimal] = mapped_column(Numeric(30, 12), nullable=False)
    high: Mapped[Decimal] = mapped_column(Numeric(30, 12), nullable=False)
    low: Mapped[Decimal] = mapped_column(Numeric(30, 12), nullable=False)
    close: Mapped[Decimal] = mapped_column(Numeric(30, 12), nullable=False)

    volume: Mapped[Decimal] = mapped_column(
        Numeric(30, 12),
        nullable=False,
        default=0,
        server_default="0",
    )
