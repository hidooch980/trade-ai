from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.trading_account import AccountKind, AccountPlatform, AccountStatus


class AccountRegisterRequest(BaseModel):
    """
    Registering a MetaTrader account.

    `password` is held only long enough to reach the credential vault; it is
    never written to the database and never appears in a response.
    """

    name: str = Field(min_length=1, max_length=100)
    server: str = Field(min_length=1, max_length=120)
    login: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)
    account_kind: AccountKind = AccountKind.DEMO
    platform: AccountPlatform = AccountPlatform.MT5
    broker: str | None = Field(default=None, max_length=100)
    currency: str = Field(default="USD", min_length=2, max_length=10)
    make_default: bool = False


class AccountUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    broker: str | None = Field(default=None, max_length=100)
    make_default: bool | None = None


class AccountCredentialsRequest(BaseModel):
    """Re-supplying the password after a restart cleared the vault."""

    password: str = Field(min_length=1, max_length=256)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    platform: str
    broker: str | None
    server: str | None
    login: str | None
    account_kind: str
    status: str
    is_default: bool
    currency: str
    balance: Decimal
    equity: Decimal
    leverage: int | None
    # Whether the vault currently holds a password for this account. The
    # reference itself is a capability and is never sent to a client.
    has_credentials: bool
    last_connected_at: datetime | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime


class AccountListResponse(BaseModel):
    items: list[AccountResponse]
    total: int
    # The MT5 adapter runs against the in-process bridge, not a terminal.
    mode: str


class AccountConnectionResponse(BaseModel):
    account: AccountResponse
    connected: bool
    status: str
    mode: str
    detail: str | None = None


__all__ = [
    "AccountConnectionResponse",
    "AccountCredentialsRequest",
    "AccountKind",
    "AccountListResponse",
    "AccountPlatform",
    "AccountRegisterRequest",
    "AccountResponse",
    "AccountStatus",
    "AccountUpdateRequest",
]
