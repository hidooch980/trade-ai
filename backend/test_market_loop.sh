#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

echo "=== BEFORE ==="
python3 - <<'PY'
from app.learning.market_memory import market_memory
print(len(market_memory.get_history()))
PY

echo "=== RUN SIGNAL ==="

python3 - <<'PY'
from app.decision.final_decision_engine import FinalDecisionEngine

engine = FinalDecisionEngine()

result = engine.decide(
    indicator_signal={"signal":"BUY"},
    ai_signal={"signal":"BUY"},
    risk={"allowed":True},
    smart_money={"pressure":"BUY"}
)

print(result)
PY


echo "=== AFTER ==="

python3 - <<'PY'
from app.learning.market_memory import market_memory
print("Memory:",len(market_memory.get_history()))
PY

echo "=== DONE ==="
