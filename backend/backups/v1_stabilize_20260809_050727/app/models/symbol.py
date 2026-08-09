from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    exchange: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    asset_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="crypto",
        server_default="crypto",
    )

    base_asset: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    quote_asset: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
