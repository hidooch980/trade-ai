"""
MetaTrader account registration and management.

Every route is scoped to the caller: an account id that belongs to someone
else answers 404, exactly as an id that does not exist.

The MT5 adapter in this build runs against the in-process bridge, which
reports itself as SIMULATION. Connecting registers the account with the
broker layer and reads balance and equity back from that bridge; it does not
reach a MetaTrader 5 terminal. Every response says so in `mode`, so nothing
here can be mistaken for live brokerage connectivity.
"""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.connection import broker_connection_manager
from app.broker.security.credential_manager import credential_manager
from app.db.session import get_db
from app.models.trading_account import (
    AccountKind,
    AccountPlatform,
    AccountStatus,
    TradingAccount,
)
from app.repositories.trading_account_repository import TradingAccountRepository
from app.schemas.accounts import (
    AccountConnectionResponse,
    AccountCredentialsRequest,
    AccountListResponse,
    AccountRegisterRequest,
    AccountResponse,
    AccountUpdateRequest,
)
from app.security.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/accounts", tags=["accounts"])

CONNECTION_TYPE = "mt5"
BRIDGE_MODE = "SIMULATION"
MAX_ACCOUNTS_PER_USER = 10


def present(account: TradingAccount) -> AccountResponse:
    return AccountResponse(
        id=account.id,
        name=account.name,
        platform=account.platform,
        broker=account.broker,
        server=account.server,
        login=account.login,
        account_kind=account.account_kind,
        status=account.status,
        is_default=account.is_default,
        currency=account.currency,
        balance=account.balance,
        equity=account.equity,
        leverage=account.leverage,
        has_credentials=bool(
            account.credential_ref and credential_manager.has(account.credential_ref)
        ),
        last_connected_at=account.last_connected_at,
        last_error=account.last_error,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )


async def load(db: AsyncSession, account_id: UUID, user_id: UUID) -> TradingAccount:
    account = await TradingAccountRepository(db).get_for_user(account_id, user_id)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account


async def commit_and_present(
    db: AsyncSession, account: TradingAccount
) -> AccountResponse:
    # updated_at carries an onupdate default, so the row has to be re-read
    # before serialisation rather than lazy-loading mid-response.
    await db.commit()
    await db.refresh(account)

    return present(account)


def broker_key(account: TradingAccount) -> str:
    """
    Which adapter the broker router should resolve.

    The account's own broker name is a label for the user; the adapter is
    chosen by platform, and MT5 is the only one wired up here.
    """
    return account.platform


@router.get("", response_model=AccountListResponse)
async def list_accounts(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    accounts = await TradingAccountRepository(db).list_by_user(current_user.id)

    return AccountListResponse(
        items=[present(a) for a in accounts],
        total=len(accounts),
        mode=BRIDGE_MODE,
    )


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def register_account(
    data: AccountRegisterRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = TradingAccountRepository(db)

    server = data.server.strip()
    login = data.login.strip()

    existing = await repository.find_existing(
        user_id=current_user.id,
        platform=data.platform.value,
        server=server,
        login=login,
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That login is already registered on this server",
        )

    if await repository.count_for_user(current_user.id) >= MAX_ACCOUNTS_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"At most {MAX_ACCOUNTS_PER_USER} accounts per user",
        )

    # The password goes to the vault and nowhere else. Only the handle is
    # persisted, and the handle never leaves the server.
    stored = credential_manager.store(
        broker=data.platform.value,
        connection_type=CONNECTION_TYPE,
        credentials={"login": login, "password": data.password, "server": server},
        metadata={"server": server, "login": login},
        owner_id=current_user.id,
    )

    first_account = await repository.count_for_user(current_user.id) == 0

    account = await repository.create(
        user_id=current_user.id,
        name=data.name.strip(),
        broker=(data.broker or "").strip() or None,
        currency=data.currency.upper(),
        platform=data.platform.value,
        server=server,
        login=login,
        account_kind=data.account_kind.value,
        credential_ref=stored["credential_id"],
        is_default=data.make_default or first_account,
    )

    if account.is_default:
        await repository.make_default(account)

    return await commit_and_present(db, account)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return present(await load(db, account_id, current_user.id))


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: UUID,
    data: AccountUpdateRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = TradingAccountRepository(db)
    account = await load(db, account_id, current_user.id)

    if data.name is not None:
        account.name = data.name.strip()

    if data.broker is not None:
        account.broker = data.broker.strip() or None

    if data.make_default:
        await repository.make_default(account)

    return await commit_and_present(db, account)


@router.put("/{account_id}/credentials", response_model=AccountResponse)
async def replace_credentials(
    account_id: UUID,
    data: AccountCredentialsRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """The vault is in memory, so a restart leaves accounts needing this."""
    account = await load(db, account_id, current_user.id)

    if account.credential_ref:
        credential_manager.delete(account.credential_ref, owner_id=current_user.id)

    stored = credential_manager.store(
        broker=account.platform,
        connection_type=CONNECTION_TYPE,
        credentials={
            "login": account.login,
            "password": data.password,
            "server": account.server,
        },
        metadata={"server": account.server, "login": account.login},
        owner_id=current_user.id,
    )

    account.credential_ref = stored["credential_id"]
    account.last_error = None

    return await commit_and_present(db, account)


@router.post("/{account_id}/connect", response_model=AccountConnectionResponse)
async def connect_account(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await load(db, account_id, current_user.id)

    if not account.credential_ref or not credential_manager.has(account.credential_ref):
        account.status = AccountStatus.ERROR.value
        account.last_error = "CREDENTIALS_REQUIRED"
        await db.commit()
        await db.refresh(account)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supply the account password again before connecting",
        )

    result = await broker_connection_manager.connect(
        broker_key(account),
        connection_type=CONNECTION_TYPE,
        credential_id=account.credential_ref,
        owner_id=current_user.id,
    )

    if not result.get("connected"):
        account.status = AccountStatus.ERROR.value
        account.last_error = str(result.get("status", "CONNECTION_FAILED"))

        return AccountConnectionResponse(
            account=await commit_and_present(db, account),
            connected=False,
            status=account.last_error,
            mode=BRIDGE_MODE,
            detail="The broker layer refused the connection",
        )

    account.status = AccountStatus.CONNECTED.value
    account.last_error = None
    account.last_connected_at = datetime.now(timezone.utc)

    # Balance and equity come back from the bridge, which is the simulator in
    # this build — recorded as reported, not presented as brokerage truth.
    snapshot = await _account_snapshot(account)

    if snapshot:
        account.balance = snapshot.get("balance", account.balance)
        account.equity = snapshot.get("equity", account.equity)
        account.currency = snapshot.get("currency", account.currency)
        account.leverage = snapshot.get("leverage", account.leverage)

    return AccountConnectionResponse(
        account=await commit_and_present(db, account),
        connected=True,
        status=str(result.get("status", "CONNECTED")),
        mode=BRIDGE_MODE,
    )


async def _account_snapshot(account: TradingAccount) -> dict | None:
    from app.broker.core.router import broker_router

    adapter_cls = broker_router.resolve(broker_key(account))

    if adapter_cls is None:
        return None

    try:
        data = await adapter_cls().get_account()
    except Exception:
        # A snapshot is a nicety; failing to read it must not fail the
        # connection that already succeeded.
        return None

    return data if isinstance(data, dict) else None


@router.post("/{account_id}/disconnect", response_model=AccountConnectionResponse)
async def disconnect_account(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await load(db, account_id, current_user.id)

    result = await broker_connection_manager.disconnect(
        broker_key(account),
        owner_id=current_user.id,
    )

    account.status = AccountStatus.DISCONNECTED.value

    return AccountConnectionResponse(
        account=await commit_and_present(db, account),
        connected=False,
        status=str(result.get("status", "DISCONNECTED")),
        mode=BRIDGE_MODE,
    )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = TradingAccountRepository(db)
    account = await load(db, account_id, current_user.id)

    was_default = account.is_default

    # Drop the connection and wipe the credentials before the row goes, so a
    # deleted account cannot leave a live session or a password behind.
    await broker_connection_manager.disconnect(
        broker_key(account),
        owner_id=current_user.id,
    )

    if account.credential_ref:
        credential_manager.delete(account.credential_ref, owner_id=current_user.id)

    await repository.delete(account)

    if was_default:
        remaining = await repository.list_by_user(current_user.id)
        if remaining:
            await repository.make_default(remaining[0])

    await db.commit()

    return None


__all__ = ["router", "AccountKind", "AccountPlatform"]
