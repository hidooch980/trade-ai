from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trading_account import TradingAccount
from app.repositories.trading_account_repository import TradingAccountRepository


class TradingAccountService:
    def __init__(self, session: AsyncSession):
        self.repository = TradingAccountRepository(session)

    async def get_by_id(self, account_id: UUID) -> TradingAccount | None:
        return await self.repository.get_by_id(account_id)

    async def list_by_user(self, user_id: UUID) -> list[TradingAccount]:
        return await self.repository.list_by_user(user_id)

    async def create(
        self,
        user_id: UUID,
        name: str,
        broker: str | None = None,
        currency: str = "USD",
    ) -> TradingAccount:
        return await self.repository.create(
            user_id=user_id,
            name=name,
            broker=broker,
            currency=currency,
        )

    async def delete(self, account: TradingAccount) -> None:
        await self.repository.delete(account)
