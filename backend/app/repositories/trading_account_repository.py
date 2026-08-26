from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trading_account import AccountPlatform, TradingAccount


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

    async def get_for_user(
        self,
        account_id: UUID,
        user_id: UUID,
    ) -> TradingAccount | None:
        """
        The only lookup a request handler should use. Filtering by owner in
        the query means a mismatched id is indistinguishable from a missing
        one, so nobody learns that someone else's account exists.
        """
        result = await self.session.execute(
            select(TradingAccount).where(
                TradingAccount.id == account_id,
                TradingAccount.user_id == user_id,
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
            .order_by(
                TradingAccount.is_default.desc(),
                TradingAccount.created_at.desc(),
            )
        )
        return list(result.scalars().all())

    async def find_existing(
        self,
        user_id: UUID,
        platform: str,
        server: str,
        login: str,
    ) -> TradingAccount | None:
        result = await self.session.execute(
            select(TradingAccount).where(
                TradingAccount.user_id == user_id,
                TradingAccount.platform == platform,
                TradingAccount.server == server,
                TradingAccount.login == login,
            )
        )
        return result.scalar_one_or_none()

    async def count_for_user(self, user_id: UUID) -> int:
        result = await self.session.execute(
            select(TradingAccount.id).where(TradingAccount.user_id == user_id)
        )
        return len(result.scalars().all())

    async def create(
        self,
        user_id: UUID,
        name: str,
        broker: str | None = None,
        currency: str = "USD",
        platform: str = AccountPlatform.MT5.value,
        server: str | None = None,
        login: str | None = None,
        account_kind: str = "DEMO",
        credential_ref: str | None = None,
        is_default: bool = False,
    ) -> TradingAccount:
        account = TradingAccount(
            user_id=user_id,
            name=name,
            broker=broker,
            currency=currency,
            platform=platform,
            server=server,
            login=login,
            account_kind=account_kind,
            credential_ref=credential_ref,
            is_default=is_default,
        )

        self.session.add(account)
        await self.session.flush()
        await self.session.refresh(account)

        return account

    async def make_default(self, account: TradingAccount) -> None:
        """Exactly one default per user, so clear the others in the same go."""
        await self.session.execute(
            update(TradingAccount)
            .where(
                TradingAccount.user_id == account.user_id,
                TradingAccount.id != account.id,
            )
            .values(is_default=False)
        )

        account.is_default = True
        await self.session.flush()

    async def delete(
        self,
        account: TradingAccount,
    ) -> None:
        await self.session.delete(account)
        await self.session.flush()
