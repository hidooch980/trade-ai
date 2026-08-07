#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_watchdog_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN WATCHDOG START ===" | tee -a $LOG

while true
do

echo "=== $(date) ===" | tee -a $LOG

echo "--- API ---" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "--- PROCESS ---" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG

echo "--- MEMORY CHECK ---" | tee -a $LOG
python - <<'PY' | tee -a $LOG
import json,glob

for f in glob.glob("app/**/*.json",recursive=True):
    try:
        json.load(open(f))
    except Exception as e:
        print("BROKEN:",f,e)

print("MEMORY SCAN DONE")
PY

echo "--- IMPORT CHECK ---" | tee -a $LOG
python - <<'PY' | tee -a $LOG
mods=[
"app.ai",
"app.decision",
"app.learning",
"app.chart_ai",
"app.execution",
"app.risk"
]

import importlib

for m in mods:
    try:
        importlib.import_module(m)
        print("OK",m)
    except Exception as e:
        print("FAIL",m,e)
PY

echo "CHECK COMPLETE" | tee -a $LOG

sleep 300

done

