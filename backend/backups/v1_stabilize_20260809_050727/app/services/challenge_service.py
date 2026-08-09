from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import (
    ChallengeAccount,
    ChallengeEvent,
    ChallengeMetric,
    ChallengePlan,
    ChallengeResult,
    ChallengeStatus,
)


class ChallengeService:

    async def get_plan(
        self,
        db: AsyncSession,
        plan_id: UUID,
    ) -> ChallengePlan | None:
        result = await db.execute(
            select(ChallengePlan).where(
                ChallengePlan.id == plan_id,
                ChallengePlan.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def list_plans(
        self,
        db: AsyncSession,
    ) -> list[ChallengePlan]:
        result = await db.execute(
            select(ChallengePlan)
            .where(ChallengePlan.is_active.is_(True))
            .order_by(ChallengePlan.starting_balance)
        )
        return list(result.scalars().all())

    async def create_challenge(
        self,
        db: AsyncSession,
        user_id: UUID,
        plan_id: UUID,
    ) -> ChallengeAccount:

        plan = await self.get_plan(db, plan_id)

        if plan is None:
            raise ValueError("Challenge plan not found")

        account_number = f"CH-{uuid4().hex[:12].upper()}"

        account = ChallengeAccount(
            user_id=user_id,
            plan_id=plan.id,
            account_number=account_number,
            status=ChallengeStatus.ACTIVE.value,
            initial_balance=plan.starting_balance,
            balance=plan.starting_balance,
            equity=plan.starting_balance,
            peak_equity=plan.starting_balance,
        )

        db.add(account)
        await db.flush()

        event = ChallengeEvent(
            challenge_account_id=account.id,
            event_type="CHALLENGE_CREATED",
            event_data={
                "plan_id": str(plan.id),
                "plan_code": plan.code,
                "starting_balance": str(plan.starting_balance),
            },
        )

        db.add(event)

        await db.commit()
        await db.refresh(account)

        return account

    async def get_account(
        self,
        db: AsyncSession,
        account_id: UUID,
    ) -> ChallengeAccount | None:

        result = await db.execute(
            select(ChallengeAccount).where(
                ChallengeAccount.id == account_id
            )
        )

        return result.scalar_one_or_none()

    async def update_account(
        self,
        db: AsyncSession,
        account_id: UUID,
        balance: Decimal,
        equity: Decimal,
        trades_count: int = 0,
    ) -> ChallengeAccount:

        account = await self.get_account(db, account_id)

        if account is None:
            raise ValueError("Challenge account not found")

        if account.status != ChallengeStatus.ACTIVE.value:
            return account

        balance = Decimal(str(balance))
        equity = Decimal(str(equity))

        account.balance = balance
        account.equity = equity

        if equity > account.peak_equity:
            account.peak_equity = equity

        plan = await self.get_plan(db, account.plan_id)

        if plan is None:
            raise ValueError("Challenge plan not found")

        initial = Decimal(str(account.initial_balance))
        peak_equity = Decimal(str(account.peak_equity))

        profit_percent = (
            ((equity - initial) / initial) * Decimal("100")
            if initial > 0
            else Decimal("0")
        )

        max_drawdown_percent = (
            ((peak_equity - equity) / peak_equity) * Decimal("100")
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
                day_start_equity=day_start_equity,
                balance=balance,
                equity=equity,
                daily_profit=Decimal("0"),
                daily_drawdown_percent=Decimal("0"),
                total_profit_percent=profit_percent,
                max_drawdown_percent=max_drawdown_percent,
                trades_count=trades_count,
            )

            db.add(metric)

        else:
            day_start_equity = Decimal(str(metric.day_start_equity))

            if day_start_equity <= 0:
                day_start_equity = equity
                metric.day_start_equity = day_start_equity

            daily_profit = equity - day_start_equity

            daily_drawdown_percent = (
                ((day_start_equity - equity) / day_start_equity)
                * Decimal("100")
                if day_start_equity > 0 and equity < day_start_equity
                else Decimal("0")
            )

            metric.balance = balance
            metric.equity = equity
            metric.daily_profit = daily_profit
            metric.daily_drawdown_percent = daily_drawdown_percent
            metric.total_profit_percent = profit_percent
            metric.max_drawdown_percent = max(
                Decimal(str(metric.max_drawdown_percent)),
                max_drawdown_percent,
            )
            metric.trades_count = trades_count

        daily_drawdown_percent = (
            ((day_start_equity - equity) / day_start_equity)
            * Decimal("100")
            if day_start_equity > 0 and equity < day_start_equity
            else Decimal("0")
        )

        failure_reason = None

        if max_drawdown_percent >= Decimal(str(plan.max_drawdown_percent)):
            failure_reason = "MAX_DRAWDOWN"

        elif daily_drawdown_percent >= Decimal(
            str(plan.daily_drawdown_percent)
        ):
            failure_reason = "DAILY_DRAWDOWN"

        elif profit_percent >= Decimal(str(plan.profit_target_percent)):
            account.status = ChallengeStatus.PASSED.value
            account.completed_at = datetime.now(timezone.utc)

            result = ChallengeResult(
                challenge_account_id=account.id,
                result="PASSED",
                profit_target_reached=True,
                daily_drawdown_ok=True,
                max_drawdown_ok=True,
                minimum_trading_days_ok=True,
                rules_ok=True,
                final_balance=balance,
                final_equity=equity,
                final_profit_percent=profit_percent,
                reason="PROFIT_TARGET_REACHED",
            )

            db.add(result)

            db.add(
                ChallengeEvent(
                    challenge_account_id=account.id,
                    event_type="CHALLENGE_PASSED",
                    event_data={
                        "profit_percent": str(profit_percent),
                    },
                )
            )

        if failure_reason:

            account.status = ChallengeStatus.FAILED.value
            account.failed_reason = failure_reason
            account.completed_at = datetime.now(timezone.utc)

            result = ChallengeResult(
                challenge_account_id=account.id,
                result="FAILED",
                profit_target_reached=False,
                daily_drawdown_ok=(
                    failure_reason != "DAILY_DRAWDOWN"
                ),
                max_drawdown_ok=(
                    failure_reason != "MAX_DRAWDOWN"
                ),
                minimum_trading_days_ok=True,
                rules_ok=False,
                final_balance=balance,
                final_equity=equity,
                final_profit_percent=profit_percent,
                reason=failure_reason,
            )

            db.add(result)

            db.add(
                ChallengeEvent(
                    challenge_account_id=account.id,
                    event_type="CHALLENGE_FAILED",
                    event_data={
                        "reason": failure_reason,
                        "daily_drawdown_percent": str(
                            daily_drawdown_percent
                        ),
                        "max_drawdown_percent": str(
                            max_drawdown_percent
                        ),
                    },
                )
            )

        await db.commit()
        await db.refresh(account)

        return account


challenge_service = ChallengeService()
