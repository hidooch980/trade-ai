from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TradingAccount(Base):
    __tablename__ = "trading_accounts"

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

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    broker: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
        server_default="USD",
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        default=0,
        server_default="0",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
