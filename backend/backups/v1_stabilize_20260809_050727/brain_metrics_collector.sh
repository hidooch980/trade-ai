#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_metrics_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI BRAIN METRICS ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import os
import json

files=[
"data/trade_journal.json",
"closed_trades.json",
"positions.json",
"app/learning/data/reward_memory.json",
"app/learning/data/strategy_memory_v2.json"
]

for f in files:
    if os.path.exists(f):
        try:
            data=json.load(open(f))
            if isinstance(data,list):
                print(f,":",len(data),"records")
            elif isinstance(data,dict):
                print(f,":",len(data),"keys")
            else:
                print(f,": loaded")
        except Exception as e:
            print(f,": ERROR",e)
    else:
        print(f,": NOT FOUND")


print("======================")
print("METRICS COLLECTION COMPLETE")

PY


echo "=== API STATUS ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "REPORT:$LOG"

