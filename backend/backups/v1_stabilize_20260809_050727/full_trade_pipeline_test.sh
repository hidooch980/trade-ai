#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

python3 - <<'PY'
import asyncio
import json

from app.market.loop.live_market_runner import live_market_runner
from app.learning.market_memory import market_memory


async def test():

    print("=== FULL TRADE PIPELINE TEST ===")

    before = len(market_memory.get_history())

    tests = [
        ("EURUSD",1.1000),
        ("GBPUSD",1.2800),
        ("XAUUSD",2430),
        ("BTCUSD",63000),
    ]

    for symbol, price in tests:

        print("\n========================")
        print("SYMBOL:", symbol)

        result = await live_market_runner.run_tick(
            symbol=symbol,
            price=price,
            volume=100
        )

        signal = result["signal"]

        print("DECISION:", signal["decision"])
        print("SCORE:", signal["decision"]["score"])
        print("SMART MONEY:", signal["smart_money"]["decision"])
        print("RISK:", signal["risk"]["account"]["status"])
        print("EXECUTION:", signal["execution"])
        print("JOURNAL:", result["journal"]["decision"])


    after = len(market_memory.get_history())

    print("\n========================")
    print("MEMORY BEFORE:", before)
    print("MEMORY AFTER :", after)
    print("MEMORY ADDED :", after-before)

    print("\n=== PIPELINE OK ===")


asyncio.run(test())

PY
