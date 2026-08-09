import asyncio, json
from app.trading.pipeline.signal_pipeline import SignalPipeline
from app.execution.position_store import position_store
from app.execution.position_monitor import position_monitor
from app.execution.trade_history import trade_history
from app.ai.learning.trade_learning_engine import trade_learning_engine

async def main():
    print("=== FULL TRADE AI CYCLE ===")

    pipeline = SignalPipeline()

    result = await pipeline.generate(
        "BTCUSDT",
        115000
    )

    print("\nSIGNAL:")
    print(result.get("decision"))

    print("\nEXECUTION:")
    print(result.get("execution"))

    print("\nPOSITIONS:")
    print(position_store.get_all())

    print("\nPRICE MOVE TEST")
    position_monitor.update(116000)

    print("\nAFTER MONITOR:")
    print(position_store.get_all())

    print("\nHISTORY:")
    print(trade_history.closed_trades)

    print("\nLEARNING:")
    print(trade_learning_engine.analyze())

asyncio.run(main())
