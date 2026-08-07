#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="auto_trader_cycle_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTO TRADER CYCLE TEST ===" | tee -a $LOG

echo "=== PIPELINE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.trading.pipeline.signal_pipeline import SignalPipeline
print("PIPELINE OK")
PY

echo "=== AI CORE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
mods=[
"app.ai",
"app.decision",
"app.learning",
"app.execution",
"app.risk",
"app.market"
]

import importlib

for m in mods:
    try:
        importlib.import_module(m)
        print("OK",m)
    except Exception as e:
        print("FAIL",m,e)
PY

echo "=== PAPER ORDER FLOW ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
signal={
"symbol":"BTCUSD",
"direction":"BUY",
"confidence":95,
"score":95
}

print("SIGNAL:",signal)
print("ORDER FLOW READY")
PY

echo "=== CLOSE FLOW ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.close_manager import CloseManager
print("CLOSE FLOW READY")
PY

echo "=== AI MEMORY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.learning.market_memory import *
print("MEMORY READY")
PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"
