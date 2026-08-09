#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="mt5_bridge_test_$(date +%Y%m%d_%H%M%S).log"

echo "=== MT5 BRIDGE TEST ===" | tee -a $LOG

echo "=== BRIDGE IMPORT ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.market.bridge.mt5_bridge import *
print("MT5 BRIDGE IMPORT OK")
PY

echo "=== EXECUTION BRIDGE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
try:
    from app.execution.metatrader_bridge import *
    print("METATRADER EXECUTION BRIDGE OK")
except Exception as e:
    print("BRIDGE ERROR:", e)
PY

echo "=== ORDER OBJECT TEST ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
order={
"symbol":"BTCUSD",
"type":"BUY",
"volume":0.01,
"mode":"PAPER"
}

print("ORDER CREATED")
print(order)
PY

echo "=== RISK CHECK ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.risk.risk_manager import RiskManager
print("RISK MODULE READY")
PY

echo "=== REPORT ==="
echo "$LOG"
