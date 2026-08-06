from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_candle import MarketCandle
from app.repositories.market_candle_repository import MarketCandleRepository


class MarketCandleService:
    def __init__(self, session: AsyncSession):
        self.repository = MarketCandleRepository(session)

    async def get_latest(
        self,
        symbol_id: UUID,
        timeframe: str,
    ) -> MarketCandle | None:
        return await self.repository.get_latest(
            symbol_id=symbol_id,
            timeframe=timeframe,
        )

    async def list_range(
        self,
        symbol_id: UUID,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 1000,
    ) -> list[MarketCandle]:
        return await self.repository.list_range(
            symbol_id=symbol_id,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def create(
        self,
        symbol_id: UUID,
        timeframe: str,
        open_time: datetime,
        open_price,
        high,
        low,
        close,
        volume=0,
        close_time=None,
    ) -> MarketCandle:
        if high < low:
            raise ValueError("Candle high cannot be lower than low")

        if open_price < low or open_price > high:
            raise ValueError("Candle open must be between low and high")

        if close < low or close > high:
            raise ValueError("Candle close must be between low and high")

        if volume < 0:
            raise ValueError("Candle volume cannot be negative")

        return await self.repository.create(
            symbol_id=symbol_id,
            timeframe=timeframe,
            open_time=open_time,
            open_price=open_price,
            high=high,
            low=low,
            close=close,
            volume=volume,
            close_time=close_time,
        )
