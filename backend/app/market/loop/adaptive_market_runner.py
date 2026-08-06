from app.market.loop.live_market_runner import live_market_runner
from app.ai.memory.strategy_memory import strategy_memory


class AdaptiveMarketRunner:


    async def run(
        self,
        symbol,
        timeframe,
        price,
        volume=0
    ):

        strategy = strategy_memory.get(
            symbol,
            timeframe
        )


        result = await live_market_runner.run_tick(
            symbol,
            price,
            volume
        )


        result["strategy"] = strategy


        return result


adaptive_market_runner = AdaptiveMarketRunner()
