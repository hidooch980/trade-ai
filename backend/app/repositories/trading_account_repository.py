from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trading_account import TradingAccount


class TradingAccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        account_id: UUID,
    ) -> TradingAccount | None:
        result = await self.session.execute(
            select(TradingAccount).where(
                TradingAccount.id == account_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
    ) -> list[TradingAccount]:
        result = await self.session.execute(
            select(TradingAccount)
            .where(TradingAccount.user_id == user_id)
            .order_by(TradingAccount.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        user_id: UUID,
        name: str,
        broker: str | None = None,
        currency: str = "USD",
    ) -> TradingAccount:
        account = TradingAccount(
            user_id=user_id,
            name=name,
            broker=broker,
            currency=currency,
        )

        self.session.add(account)
        await self.session.flush()
        await self.session.refresh(account)

        return account

    async def delete(
        self,
        account: TradingAccount,
    ) -> None:
        await self.session.delete(account)
        await self.session.flush()
