"""
The risk brain, over HTTP.

Read and edit an account's limits, see how much room is left under each one,
and ask whether a trade you are considering would be allowed before you send
it. Every route is scoped to the caller; an account belonging to someone else
answers 404.

Positions come from the request rather than the engine's position store,
because that store is not partitioned per account in this build — reading it
here would fold other people's trades into your risk picture.
"""

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.risk_policy import AccountRiskPolicy
from app.models.trading_account import TradingAccount
from app.repositories.trading_account_repository import TradingAccountRepository
from app.risk.brain import (
    AccountSnapshot,
    PositionView,
    ProposedTrade,
    RiskPolicy,
    RiskVerdict,
)
from app.risk.brain import risk_brain
from app.schemas.risk import (
    AssessRequest,
    RiskAssessmentResponse,
    RiskPolicyPayload,
    RiskPolicyResponse,
    RuleResultResponse,
)
from app.security.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/risk", tags=["risk"])

POLICY_FIELDS = (
    "max_daily_loss_percent",
    "max_total_loss_percent",
    "max_risk_per_trade_percent",
    "max_open_positions",
    "max_total_exposure_ratio",
    "max_symbol_exposure_percent",
    "max_correlated_positions",
    "warn_at_percent",
)


async def load_account(
    db: AsyncSession, account_id: UUID, user_id: UUID
) -> TradingAccount:
    account = await TradingAccountRepository(db).get_for_user(account_id, user_id)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account


async def _select_policy(
    db: AsyncSession, account_id: UUID
) -> AccountRiskPolicy | None:
    result = await db.execute(
        select(AccountRiskPolicy).where(
            AccountRiskPolicy.account_id == account_id
        )
    )
    return result.scalar_one_or_none()


async def load_policy(
    db: AsyncSession, account: TradingAccount
) -> AccountRiskPolicy:
    """
    The stored policy, created with defaults the first time it is needed.

    The dashboard asks for the state and the policy at the same time, so two
    requests can reach an account with no policy row at once. The insert runs
    in a savepoint: whichever request loses the unique constraint rolls back
    only that statement and reads the row the winner wrote.
    """
    policy = await _select_policy(db, account.id)

    if policy is not None:
        return policy

    opening = account.equity or account.balance

    try:
        async with db.begin_nested():
            policy = AccountRiskPolicy(
                account_id=account.id,
                day_start_equity=opening,
                day_started_at=datetime.now(timezone.utc),
                peak_equity=opening,
            )
            db.add(policy)
            await db.flush()
    except IntegrityError:
        policy = await _select_policy(db, account.id)

        if policy is None:
            raise

        return policy

    await db.refresh(policy)

    return policy


def to_brain_policy(row: AccountRiskPolicy) -> RiskPolicy:
    return RiskPolicy(
        max_daily_loss_percent=row.max_daily_loss_percent,
        max_total_loss_percent=row.max_total_loss_percent,
        max_risk_per_trade_percent=row.max_risk_per_trade_percent,
        max_open_positions=row.max_open_positions,
        max_total_exposure_ratio=row.max_total_exposure_ratio,
        max_symbol_exposure_percent=row.max_symbol_exposure_percent,
        max_correlated_positions=row.max_correlated_positions,
        warn_at_percent=row.warn_at_percent,
    )


def present_policy(row: AccountRiskPolicy) -> RiskPolicyResponse:
    return RiskPolicyResponse(
        account_id=str(row.account_id),
        max_daily_loss_percent=row.max_daily_loss_percent,
        max_total_loss_percent=row.max_total_loss_percent,
        max_risk_per_trade_percent=row.max_risk_per_trade_percent,
        max_open_positions=row.max_open_positions,
        max_total_exposure_ratio=row.max_total_exposure_ratio,
        max_symbol_exposure_percent=row.max_symbol_exposure_percent,
        max_correlated_positions=row.max_correlated_positions,
        warn_at_percent=row.warn_at_percent,
        day_start_equity=row.day_start_equity,
        day_started_at=row.day_started_at,
        peak_equity=row.peak_equity,
        updated_at=row.updated_at,
    )


def present_verdict(
    account: TradingAccount,
    snapshot: AccountSnapshot,
    verdict: RiskVerdict,
) -> RiskAssessmentResponse:
    return RiskAssessmentResponse(
        account_id=str(account.id),
        decision=verdict.decision.value,
        allowed=verdict.allowed,
        reasons=list(verdict.reasons),
        equity=snapshot.equity,
        day_start_equity=snapshot.day_reference,
        peak_equity=snapshot.peak_reference,
        exposure=snapshot.exposure,
        open_positions=len(snapshot.positions),
        rules=[
            RuleResultResponse(
                rule=r.rule.value,
                status=r.status.value,
                used=r.used,
                limit=r.limit,
                unit=r.unit,
                headroom=r.headroom,
                utilisation_percent=r.utilisation_percent,
                detail=r.detail,
            )
            for r in verdict.rules
        ],
    )


@router.get("/accounts/{account_id}/policy", response_model=RiskPolicyResponse)
async def get_policy(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await load_account(db, account_id, current_user.id)
    policy = await load_policy(db, account)

    await db.commit()
    await db.refresh(policy)

    return present_policy(policy)


@router.put("/accounts/{account_id}/policy", response_model=RiskPolicyResponse)
async def update_policy(
    account_id: UUID,
    data: RiskPolicyPayload,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await load_account(db, account_id, current_user.id)
    policy = await load_policy(db, account)

    for name in POLICY_FIELDS:
        value = getattr(data, name)
        if value is not None:
            setattr(policy, name, value)

    await db.commit()
    await db.refresh(policy)

    return present_policy(policy)


@router.post("/accounts/{account_id}/day-reset", response_model=RiskPolicyResponse)
async def reset_day(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Starts a new trading day from the account's current equity."""
    account = await load_account(db, account_id, current_user.id)
    policy = await load_policy(db, account)

    equity = account.equity or account.balance

    policy.day_start_equity = equity
    policy.day_started_at = datetime.now(timezone.utc)

    if policy.peak_equity is None or equity > policy.peak_equity:
        policy.peak_equity = equity

    await db.commit()
    await db.refresh(policy)

    return present_policy(policy)


async def _assess(
    db: AsyncSession,
    account: TradingAccount,
    data: AssessRequest,
) -> RiskAssessmentResponse:
    policy = await load_policy(db, account)

    equity = data.equity if data.equity is not None else (account.equity or account.balance)
    equity = Decimal(str(equity))

    # A new high water mark is a fact about the account, so record it rather
    # than letting the drawdown rule quietly reset itself on the next call.
    if policy.peak_equity is None or equity > policy.peak_equity:
        policy.peak_equity = equity

    snapshot = AccountSnapshot(
        balance=account.balance,
        equity=equity,
        day_start_equity=policy.day_start_equity,
        peak_equity=policy.peak_equity,
        positions=tuple(
            PositionView(
                symbol=p.symbol,
                side=p.side,
                volume=p.volume,
                entry_price=p.entry_price,
                current_price=p.current_price,
                pnl=p.pnl,
            )
            for p in data.positions
        ),
    )

    trade = (
        ProposedTrade(
            symbol=data.trade.symbol,
            side=data.trade.side,
            volume=data.trade.volume,
            entry_price=data.trade.entry_price,
            stop_loss=data.trade.stop_loss,
        )
        if data.trade
        else None
    )

    verdict = risk_brain.assess(snapshot, to_brain_policy(policy), trade)

    await db.commit()

    return present_verdict(account, snapshot, verdict)


@router.get("/accounts/{account_id}/state", response_model=RiskAssessmentResponse)
async def risk_state(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Headroom on the account as it stands, with no trade proposed."""
    account = await load_account(db, account_id, current_user.id)

    return await _assess(db, account, AssessRequest())


@router.post("/accounts/{account_id}/assess", response_model=RiskAssessmentResponse)
async def assess(
    account_id: UUID,
    data: AssessRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Would this book, and optionally this next trade, be allowed?"""
    account = await load_account(db, account_id, current_user.id)

    return await _assess(db, account, data)
