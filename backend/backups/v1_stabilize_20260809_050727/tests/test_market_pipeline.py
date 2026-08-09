import asyncio
from app.market_data.providers.mock_provider import MockMarketDataProvider
from app.market_data.services.data_service import MarketDataService

async def main():

    provider = MockMarketDataProvider()

    service = MarketDataService(
        provider=provider
    )

    candles = await service.get_market_candles(
        "XAUUSD",
        "H1"
    )

    ticks = await service.get_market_ticks(
        "XAUUSD"
    )

    print("CANDLE PIPELINE:", candles)
    print("TICK PIPELINE:", ticks)

asyncio.run(main())
