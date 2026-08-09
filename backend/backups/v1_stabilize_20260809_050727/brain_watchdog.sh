#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_watchdog_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN WATCHDOG START ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import importlib

modules = [
"app.ai",
"app.decision",
"app.learning",
"app.chart_ai",
"app.execution",
"app.risk",
"app.market",
"app.trading.pipeline.signal_pipeline",
"app.execution.position_store",
"app.execution.close_manager"
]

healthy=0
failed=0

for m in modules:
    try:
        importlib.import_module(m)
        print("OK:",m)
        healthy+=1
    except Exception as e:
        print("FAIL:",m,e)
        failed+=1

print("================")
print("HEALTHY:",healthy)
print("FAILED:",failed)

PY

echo "=== API ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "=== PROCESS ===" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG

echo "REPORT:$LOG"

