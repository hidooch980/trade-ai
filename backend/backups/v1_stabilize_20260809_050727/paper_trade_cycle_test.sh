#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="paper_trade_cycle_$(date +%Y%m%d_%H%M%S).log"

echo "=== PAPER TRADE CYCLE ===" | tee -a $LOG

echo "=== POSITION STORE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.position_store import position_store

position={
"ticket":"PAPER-TEST-001",
"symbol":"BTCUSD",
"side":"BUY",
"volume":0.01,
"entry":50000,
"status":"OPEN"
}

position_store.add(position)

print("POSITION ADDED")
print(position_store)
PY

echo "=== CLOSE SIMULATION ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.close_manager import CloseManager

print("CLOSE MANAGER READY")
print(CloseManager)
PY

echo "=== TRADE HISTORY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.trade_history import TradeHistory

print("HISTORY READY")
print(TradeHistory)
PY

echo "=== MEMORY UPDATE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.learning.market_memory import *
print("LEARNING MEMORY READY")
PY

echo "REPORT:$LOG"
