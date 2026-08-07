#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

python3 - <<'PY'
from app.decision.master_ai_core import MasterAICore

ai = MasterAICore()

for symbol in [
    "EURUSD",
    "GBPUSD",
    "XAUUSD",
    "BTCUSD"
]:

    print("\n================")
    print(symbol)

    result = ai.decide(symbol)

    print(result)

PY
