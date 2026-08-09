import asyncio

from app.trading.pipeline.signal_pipeline import SignalPipeline
from app.execution.position_monitor import position_monitor
from app.execution.position_store import position_store
from app.execution.trade_history import trade_history


async def run_test():

    print("=== TRADE AI FULL TEST ===")

    pipeline = SignalPipeline()

    symbol = "BTCUSDT"
    price = 115000


    print("\n1) Generate Signal")

    result = await pipeline.generate(
        symbol,
        price
    )

    print(
        "Decision:",
        result.get("decision")
    )


    print(
        "Execution:",
        result.get("execution")
    )


    print("\n2) Current Positions")

    print(
        position_store.get_all()
    )


    print("\n3) Simulate Price Move")

    position_monitor.update(
        price + 500
    )


    print(
        "Positions After Monitor:"
    )

    print(
        position_store.get_all()
    )


    print("\n4) Trade History")

    print(
        trade_history.closed_trades
    )


if __name__ == "__main__":
    asyncio.run(run_test())
