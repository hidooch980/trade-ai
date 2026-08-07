#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_recovery_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN RECOVERY TEST ===" | tee -a $LOG

echo "=== BEFORE RESTART HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "=== MEMORY BEFORE ===" | tee -a $LOG
ls -lh app/learning/data/*.json | tee -a $LOG

echo "=== PROCESS ===" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG

echo "=== IMPORT AFTER SIMULATION ===" | tee -a $LOG
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
        print("RECOVERY OK:",m)
    except Exception as e:
        print("RECOVERY FAIL:",m,e)
PY

echo "=== MEMORY AFTER ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
import json

files=[
"app/learning/data/market_memory.json",
"app/learning/data/reward_memory.json",
"app/learning/data/strategy_memory_v2.json"
]

for f in files:
    try:
        json.load(open(f))
        print("MEMORY OK:",f)
    except Exception as e:
        print("MEMORY ERROR:",f,e)
PY

echo "=== FINAL HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"
