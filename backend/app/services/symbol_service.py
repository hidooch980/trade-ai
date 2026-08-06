from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symbol import Symbol
from app.repositories.symbol_repository import SymbolRepository


class SymbolService:
    def __init__(self, session: AsyncSession):
        self.repository = SymbolRepository(session)

    async def get_by_id(self, symbol_id):
        return await self.repository.get_by_id(symbol_id)

    async def get_by_exchange_and_symbol(
        self,
        exchange: str,
        symbol: str,
    ) -> Symbol | None:
        return await self.repository.get_by_exchange_and_symbol(
            exchange=exchange,
            symbol=symbol,
        )

    async def list_by_exchange(self, exchange: str) -> list[Symbol]:
        return await self.repository.list_by_exchange(exchange)

    async def create(
        self,
        exchange: str,
        symbol: str,
        asset_type: str = "crypto",
        base_asset: str | None = None,
        quote_asset: str | None = None,
    ) -> Symbol:
        existing = await self.repository.get_by_exchange_and_symbol(
            exchange=exchange,
            symbol=symbol,
        )

        if existing:
            raise ValueError("Symbol already exists for this exchange")

        return await self.repository.create(
            exchange=exchange,
            symbol=symbol,
            asset_type=asset_type,
            base_asset=base_asset,
            quote_asset=quote_asset,
        )
