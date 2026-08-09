import asyncio

from app.trading.pipeline.signal_pipeline import signal_pipeline
from app.execution.order_flow import order_flow
from app.execution.position_store import position_store


async def main():

    print("===== SIGNAL PIPELINE TEST =====")

    result = await signal_pipeline.run(
        {
            "symbol": "EURUSD",
            "timeframe": "M1",
            "price": 1.1000
        }
    )

    print("\nSIGNAL RESULT:")
    print(result)


    print("\n===== ORDER FLOW TEST =====")

    if result.get("decision"):

        order = await order_flow.process(
            result["symbol"],
            {
                "decision": result["decision"]
            },
            {
                "approved": True,
                "volume": 1,
                "entry_price": result.get("price",1.1),
                "stop_loss": 1.09,
                "take_profit": 1.11
            }
        )

        print(order)

    else:
        print("NO TRADE SIGNAL")


    print("\n===== POSITIONS =====")
    print(position_store.get_all())


asyncio.run(main())
