from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import (
    ChallengeAccount,
    ChallengeMetric,
    ChallengePlan,
    ChallengeStatus,
)


class ChallengeGuard:
    """
    Challenge execution guard.

    Rules:
    - Only ACTIVE challenges may trade.
    - Max Drawdown is calculated from Peak Equity.
    - Daily Drawdown is calculated from the persisted start-of-day equity.
    - The first validation of a new trading day initializes day_start_equity.
    """

    async def validate(
        self,
        db: AsyncSession,
        account_id: UUID,
        balance: Decimal,
        equity: Decimal,
    ) -> dict:

        result = await db.execute(
            select(ChallengeAccount).where(
                ChallengeAccount.id == account_id
            )
        )
        account = result.scalar_one_or_none()

        if account is None:
            return {
                "allowed": False,
                "reason": "CHALLENGE_ACCOUNT_NOT_FOUND",
            }

        if account.status != ChallengeStatus.ACTIVE.value:
            return {
                "allowed": False,
                "reason": f"CHALLENGE_{account.status}",
                "status": account.status,
            }

        plan_result = await db.execute(
            select(ChallengePlan).where(
                ChallengePlan.id == account.plan_id
            )
        )
        plan = plan_result.scalar_one_or_none()

        if plan is None:
            return {
                "allowed": False,
                "reason": "CHALLENGE_PLAN_NOT_FOUND",
            }

        balance = Decimal(str(balance))
        equity = Decimal(str(equity))

        peak_equity = Decimal(str(account.peak_equity))

        if equity > peak_equity:
            peak_equity = equity

        max_drawdown = (
            ((peak_equity - equity) / peak_equity)
            * Decimal("100")
            if peak_equity > 0
            else Decimal("0")
        )

        today = date.today()

        metric_result = await db.execute(
            select(ChallengeMetric).where(
                ChallengeMetric.challenge_account_id == account.id,
                ChallengeMetric.trading_date == today,
            )
        )
        metric = metric_result.scalar_one_or_none()

        if metric is None:
            day_start_equity = equity

            metric = ChallengeMetric(
                challenge_account_id=account.id,
                trading_date=today,
                balance=balance,
                equity=equity,
                day_start_equity=day_start_equity,
                daily_profit=Decimal("0"),
                daily_drawdown_percent=Decimal("0"),
                total_profit_percent=(
                    ((equity - Decimal(str(account.initial_balance)))
                     / Decimal(str(account.initial_balance)))
                    * Decimal("100")
                    if Decimal(str(account.initial_balance)) > 0
                    else Decimal("0")
                ),
                max_drawdown_percent=max_drawdown,
                trades_count=0,
            )

            db.add(metric)
            await db.flush()

        else:
            day_start_equity = Decimal(str(metric.day_start_equity))

            if day_start_equity <= 0:
                day_start_equity = equity
                metric.day_start_equity = day_start_equity

        daily_drawdown = (
            ((day_start_equity - equity) / day_start_equity)
            * Decimal("100")
            if day_start_equity > 0 and equity < day_start_equity
            else Decimal("0")
        )

        if max_drawdown >= Decimal(str(plan.max_drawdown_percent)):
            return {
                "allowed": False,
                "reason": "MAX_DRAWDOWN_LIMIT",
                "status": ChallengeStatus.FAILED.value,
                "max_drawdown_percent": str(max_drawdown),
                "daily_drawdown_percent": str(daily_drawdown),
                "day_start_equity": str(day_start_equity),
                "limit_percent": str(plan.max_drawdown_percent),
            }

        if daily_drawdown >= Decimal(
            str(plan.daily_drawdown_percent)
        ):
            return {
                "allowed": False,
                "reason": "DAILY_DRAWDOWN_LIMIT",
                "status": ChallengeStatus.FAILED.value,
                "max_drawdown_percent": str(max_drawdown),
                "daily_drawdown_percent": str(daily_drawdown),
                "day_start_equity": str(day_start_equity),
                "limit_percent": str(plan.daily_drawdown_percent),
            }

        metric.balance = balance
        metric.equity = equity
        metric.daily_drawdown_percent = daily_drawdown
        metric.max_drawdown_percent = max(
            Decimal(str(metric.max_drawdown_percent)),
            max_drawdown,
        )

        await db.commit()

        return {
            "allowed": True,
            "status": ChallengeStatus.ACTIVE.value,
            "max_drawdown_percent": str(max_drawdown),
            "daily_drawdown_percent": str(daily_drawdown),
            "day_start_equity": str(day_start_equity),
        }


challenge_guard = ChallengeGuard()
