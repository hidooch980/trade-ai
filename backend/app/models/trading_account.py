from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    false as sa_false,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AccountPlatform(str, Enum):
    MT5 = "MT5"


class AccountKind(str, Enum):
    DEMO = "DEMO"
    REAL = "REAL"


class AccountStatus(str, Enum):
    """Where a registered account stands with its broker."""

    PENDING = "PENDING"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"


class TradingAccount(Base):
    __tablename__ = "trading_accounts"

    __table_args__ = (
        # The same terminal login on the same server is one account, not two.
        UniqueConstraint(
            "user_id",
            "platform",
            "server",
            "login",
            name="uq_trading_accounts_user_platform_server_login",
        ),
        Index("ix_trading_accounts_user_status", "user_id", "status"),
    )

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

    platform: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=AccountPlatform.MT5.value,
        server_default=AccountPlatform.MT5.value,
    )

    # MetaTrader server name, e.g. "ICMarketsSC-Demo".
    server: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    # The terminal login number. Stored as text: it is an identifier, not a
    # quantity, and brokers are not consistent about its width.
    login: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    account_kind: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default=AccountKind.DEMO.value,
        server_default=AccountKind.DEMO.value,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=AccountStatus.PENDING.value,
        server_default=AccountStatus.PENDING.value,
    )

    is_default: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=sa_false(),
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

    equity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        default=0,
        server_default="0",
        nullable=False,
    )

    leverage: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Handle into the in-memory credential vault. The terminal password is
    # never written to this table, and this reference is never returned to a
    # client — it is a capability, not an identifier.
    credential_ref: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
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
