import asyncio
from app.market.feed.simulation_feed import SimulationFeed
from app.market_data.candles.candle_manager import candle_manager
from app.trading.pipeline.signal_pipeline import SignalPipeline

class MarketLoop:

    def __init__(self):
        self.feed = SimulationFeed()
        self.pipeline = SignalPipeline()

    async def run(self):
        while True:
            candles = await self.feed.get_candles(
                "XAUUSD",
                "M5",
                5
            )

            for c in candles:
                candle_manager.push(
                    c.symbol,
                    c.open,
                    c.high,
                    c.low,
                    c.close,
                    c.volume,
                    c.timeframe,
                    c.timestamp
                )

            signal = self.pipeline.generate(
                "XAUUSD",
                candles[-1].close
            )

            print(signal["decision"])

            await asyncio.sleep(10)


market_loop = MarketLoop()
