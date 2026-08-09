from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func, Index
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_email", "email", unique=False),
        Index("ix_users_username", "username", unique=False),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(String(10), nullable=False, server_default="en", default="en")

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="CUSTOMER",
        default="CUSTOMER",
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        nullable=False,
        server_default="0",
        default=0,
    )

    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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
