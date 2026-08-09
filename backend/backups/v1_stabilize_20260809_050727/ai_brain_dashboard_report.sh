#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="ai_brain_dashboard_$(date +%Y%m%d_%H%M%S).log"

echo "================================" | tee -a $LOG
echo "        AI BRAIN DASHBOARD      " | tee -a $LOG
echo "================================" | tee -a $LOG

echo "" | tee -a $LOG
echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "" | tee -a $LOG
echo "=== ADAPTIVE MEMORY ===" | tee -a $LOG

if [ -f app/ai/memory/adaptive_strategy_weights.json ]
then
cat app/ai/memory/adaptive_strategy_weights.json | tee -a $LOG
else
echo "NOT FOUND" | tee -a $LOG
fi


echo "" | tee -a $LOG
echo "=== AI PERFORMANCE ===" | tee -a $LOG

if [ -f app/ai/memory/ai_performance.json ]
then
cat app/ai/memory/ai_performance.json | tee -a $LOG
else
echo "NOT FOUND" | tee -a $LOG
fi


echo "" | tee -a $LOG
echo "=== TRADE MEMORY ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json,os

files=[
"closed_trades.json",
"positions.json",
"app/learning/data/reward_memory.json"
]

for f in files:
    if os.path.exists(f):
        try:
            d=json.load(open(f))
            print(f,":",len(d) if hasattr(d,"__len__") else "OK")
        except Exception as e:
            print(f,"ERROR",e)
PY


echo "" | tee -a $LOG
echo "=== PROCESS ===" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG


echo "" | tee -a $LOG
echo "REPORT:$LOG"

