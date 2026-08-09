import asyncio
from app.market.loop.live_market_runner import live_market_runner
from app.market.feed import feed_factory
from app.market.market_monitor import market_monitor

price_provider = feed_factory.create('SIMULATION')

class MarketStreamWorker:
    def __init__(self):
        self.running = False

    async def start(self, symbol="XAUUSD"):
        self.running = True
        while self.running:
            tick = await price_provider.get_price(symbol)
            result = await live_market_runner.run_tick(
                tick["symbol"],
                tick["price"],
                tick["volume"]
            )
            market_monitor.update_price({
                tick["symbol"]: tick["price"]
            })
            print("STREAM:", result["signal"]["decision"], tick["price"])
            await asyncio.sleep(5)

    def stop(self):
        self.running = False

market_stream_worker = MarketStreamWorker()
