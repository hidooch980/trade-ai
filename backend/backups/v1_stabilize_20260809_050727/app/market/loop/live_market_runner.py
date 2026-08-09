import asyncio

from app.market_data.live.tick_feed import tick_feed
from app.market_data.store.market_store import market_store
from app.market_data.candle.candle_builder import candle_builder
from app.trading.pipeline.signal_pipeline import SignalPipeline
from app.api.websocket.socket_manager import socket_manager
from app.ai.journal.journal_connector import journal_connector
from app.execution.position_monitor import position_monitor
from app.execution.close_manager import close_manager


class LiveMarketRunner:

    def __init__(self):
        self.pipeline = SignalPipeline()

    async def run_tick(
        self,
        symbol,
        price,
        volume=0
    ):

        tick = tick_feed.update(
            symbol,
            price,
            volume
        )

        candle_builder.update(
            symbol,
            price,
            volume,
            timeframe="M1"
        )


        result = await self.pipeline.generate(
            symbol,
            price
        )

        print("EXECUTION:", result.get("execution"))

        positions = await self.pipeline.executor.mt5.get_positions_with_pnl(price=price)

        print("POSITIONS:", positions)

        close_actions = position_monitor.check(
            await self.pipeline.executor.mt5.get_positions(),
            {symbol: price}
        )

        if close_actions:
            print("CLOSE ACTIONS:", close_actions)

            for action in close_actions:
                close_result = await close_manager.close(
                    self.pipeline.executor.mt5,
                    action["ticket"],
                    exit_price=action.get("price"),
                    reason=action.get("reason", "EXIT_TRIGGERED")
                )

                print("CLOSE RESULT:", close_result)

        journal = None

        decision = (
            result.get("decision", {})
            if isinstance(result, dict)
            else {}
        )

        if decision.get("decision") in ("BUY", "SELL"):
            journal = journal_connector.save_signal(result)

        payload = {
            "tick": tick,
            "signal": result,
            "journal": journal
        }

        await socket_manager.broadcast(
            payload
        )

        return payload


live_market_runner = LiveMarketRunner()
