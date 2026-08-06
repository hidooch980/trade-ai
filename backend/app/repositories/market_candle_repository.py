from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_candle import MarketCandle


class MarketCandleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_latest(
        self,
        symbol_id: UUID,
        timeframe: str,
    ) -> MarketCandle | None:
        result = await self.session.execute(
            select(MarketCandle)
            .where(
                MarketCandle.symbol_id == symbol_id,
                MarketCandle.timeframe == timeframe,
            )
            .order_by(MarketCandle.open_time.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_range(
        self,
        symbol_id: UUID,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 1000,
    ) -> list[MarketCandle]:
        result = await self.session.execute(
            select(MarketCandle)
            .where(
                MarketCandle.symbol_id == symbol_id,
                MarketCandle.timeframe == timeframe,
                MarketCandle.open_time >= start_time,
                MarketCandle.open_time <= end_time,
            )
            .order_by(MarketCandle.open_time.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

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
        candle = MarketCandle(
            symbol_id=symbol_id,
            timeframe=timeframe,
            open_time=open_time,
            close_time=close_time,
            open=open_price,
            high=high,
            low=low,
            close=close,
            volume=volume,
        )

        self.session.add(candle)
        await self.session.flush()
        await self.session.refresh(candle)

        return candle
