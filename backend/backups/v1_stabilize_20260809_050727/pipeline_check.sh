#!/bin/bash
cd /opt/trade-ai/backend || exit 1
echo "=== PIPELINE FILES ==="
ls app/trading/pipeline
echo "=== DECISION ==="
ls app/decision
echo "=== EXECUTION ==="
ls app/execution
echo "=== POSITION ==="
python - <<'PY'
from app.execution.position_store import position_store
print(position_store)
try:
    print("POSITIONS:", position_store.get_all())
except Exception as e:
    print("POSITION ERROR:",e)
PY
echo "=== DONE ==="
