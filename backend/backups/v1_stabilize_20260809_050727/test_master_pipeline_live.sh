#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

python3 - <<'PY'
import asyncio

from app.market.loop.live_market_runner import live_market_runner
from app.learning.market_memory import market_memory


async def test():

    before = len(market_memory.get_history())

    for symbol, price in [
        ("EURUSD",1.1000),
        ("GBPUSD",1.2800),
        ("XAUUSD",2430),
        ("BTCUSD",63000)
    ]:

        print("\n================")
        print("SYMBOL:", symbol)

        result = await live_market_runner.run_tick(
            symbol=symbol,
            price=price,
            volume=100
        )

        signal = result["signal"]

        print("FINAL:", signal["decision"])
        print("SMART:", signal["smart_money"])
        print("EXECUTION:", signal["execution"])
        print("JOURNAL:", result["journal"])


    after = len(market_memory.get_history())

    print("\n================")
    print("MEMORY BEFORE:", before)
    print("MEMORY AFTER :", after)
    print("ADDED:", after-before)


asyncio.run(test())
PY
