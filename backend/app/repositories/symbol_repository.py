from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symbol import Symbol


class SymbolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        symbol_id: UUID,
    ) -> Symbol | None:
        result = await self.session.execute(
            select(Symbol).where(Symbol.id == symbol_id)
        )
        return result.scalar_one_or_none()

    async def get_by_exchange_and_symbol(
        self,
        exchange: str,
        symbol: str,
    ) -> Symbol | None:
        result = await self.session.execute(
            select(Symbol).where(
                Symbol.exchange == exchange,
                Symbol.symbol == symbol,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_exchange(
        self,
        exchange: str,
    ) -> list[Symbol]:
        result = await self.session.execute(
            select(Symbol)
            .where(Symbol.exchange == exchange)
            .order_by(Symbol.symbol.asc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        exchange: str,
        symbol: str,
        asset_type: str = "crypto",
        base_asset: str | None = None,
        quote_asset: str | None = None,
    ) -> Symbol:
        item = Symbol(
            exchange=exchange,
            symbol=symbol,
            asset_type=asset_type,
            base_asset=base_asset,
            quote_asset=quote_asset,
        )

        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)

        return item
