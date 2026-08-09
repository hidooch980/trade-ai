#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

python3 - <<'PY'
import asyncio

from app.decision.master_ai_core import MasterAICore
from app.market.loop.live_market_runner import live_market_runner
from app.learning.technical_analyzer import technical_analyzer
from app.learning.market_memory import market_memory


async def test():

    print("=== FULL AI BRAIN V2 TEST ===")

    before = len(market_memory.get_history())

    ai = MasterAICore()

    for symbol, price in [
        ("EURUSD",1.1000),
        ("GBPUSD",1.2800),
        ("XAUUSD",2430),
        ("BTCUSD",63000)
    ]:

        print("\n====================")
        print("SYMBOL:", symbol)

        tech = technical_analyzer.calculate(symbol)

        print("TECH:")
        print(tech)

        master = ai.decide(symbol)

        print("\nMASTER AI:")
        print(master)

        live = await live_market_runner.run_tick(
            symbol=symbol,
            price=price,
            volume=100
        )

        print("\nFINAL:")
        print(live["signal"]["decision"])

        print("SMART:")
        print(live["signal"]["smart_money"])

        print("EXECUTION:")
        print(live["signal"]["execution"])


    after = len(market_memory.get_history())

    print("\n====================")
    print("MEMORY BEFORE:", before)
    print("MEMORY AFTER :", after)
    print("ADDED:", after-before)

    print("\n=== TEST COMPLETE ===")


asyncio.run(test())

PY
