#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

echo "=== TRADE AI FULL BRAIN TEST ==="

python3 - <<'PY'
import asyncio

from app.decision.final_decision_engine import FinalDecisionEngine
from app.learning.market_memory import market_memory
from app.market.loop.live_market_runner import live_market_runner


print("\n=== MEMORY BEFORE ===")
before = len(market_memory.get_history())
print(before)


print("\n=== FINAL DECISION ENGINE TEST ===")

engine = FinalDecisionEngine()

tests = [
    {
        "name":"STRONG BUY",
        "indicator":{"decision":"BUY"},
        "ai":{"decision":"BUY"},
        "risk":{"approved":True},
        "smart":{"decision":"BUY"}
    },
    {
        "name":"STRONG SELL",
        "indicator":{"decision":"SELL"},
        "ai":{"decision":"SELL"},
        "risk":{"approved":True},
        "smart":{"decision":"SELL"}
    },
    {
        "name":"WAIT",
        "indicator":{"decision":"WAIT"},
        "ai":{"decision":"WAIT"},
        "risk":{"approved":True},
        "smart":{"decision":"WAIT"}
    }
]


for t in tests:
    result = engine.decide(
        t["indicator"],
        t["ai"],
        t["risk"],
        t["smart"]
    )

    print("\nTEST:", t["name"])
    print(result)


async def live_test():

    print("\n=== LIVE MARKET TEST ===")

    result = await live_market_runner.run_tick(
        symbol="EURUSD",
        price=1.0925,
        volume=100
    )

    print("\nLIVE RESULT")
    print(result["signal"]["decision"])

    print("SMART MONEY:")
    print(result["signal"]["smart_money"])

    print("EXECUTION:")
    print(result["signal"]["execution"])


asyncio.run(live_test())


print("\n=== MEMORY AFTER ===")
after = len(market_memory.get_history())
print(after)

print("\nMEMORY ADDED:", after-before)

print("\n=== DONE ===")

PY
