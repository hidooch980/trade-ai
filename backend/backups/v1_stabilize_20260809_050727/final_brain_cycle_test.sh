#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

python3 - <<'PY'
import asyncio

from app.market.loop.live_market_runner import live_market_runner
from app.learning.market_memory import market_memory

pairs = [
    ("EURUSD",1.0925),
    ("GBPUSD",1.2750),
    ("XAUUSD",2425),
    ("BTCUSD",62000)
]

async def test():

    before = len(market_memory.get_history())

    for symbol, price in pairs:

        print("\n================")
        print("SYMBOL:", symbol)

        result = await live_market_runner.run_tick(
            symbol=symbol,
            price=price,
            volume=100
        )

        signal = result["signal"]

        print("DECISION:", signal["decision"])
        print("SMART:", signal["smart_money"])
        print("EXECUTION:", signal["execution"])

    after = len(market_memory.get_history())

    print("\n================")
    print("MEMORY BEFORE:", before)
    print("MEMORY AFTER :", after)
    print("ADDED:", after-before)


asyncio.run(test())
PY
