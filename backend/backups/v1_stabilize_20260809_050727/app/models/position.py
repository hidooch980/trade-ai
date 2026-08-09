from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class PositionSide(str, Enum):
    LONG = "long"
    SHORT = "short"


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    account_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("trading_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    symbol_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("symbols.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    side: Mapped[PositionSide] = mapped_column(
        String(10),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=0,
        server_default="0",
    )

    entry_price: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
    )

    current_price: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 8),
        nullable=True,
    )

    realized_pnl: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=0,
        server_default="0",
    )

    unrealized_pnl: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False,
        default=0,
        server_default="0",
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
