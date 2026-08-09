
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="adaptive_trade_learning_$(date +%Y%m%d_%H%M%S).log"

echo "=== ADAPTIVE TRADE LEARNING ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

source="app/ai/memory/trade_analysis.json"
memory="app/learning/data/reward_memory.json"

if os.path.exists(source):
    analysis=json.load(open(source))
else:
    analysis={}

reward=[]

if os.path.exists(memory):
    try:
        reward=json.load(open(memory))
    except:
        reward=[]

if not isinstance(reward,list):
    reward=[]


sample={
    "time":datetime.now(timezone.utc).isoformat(),
    "accuracy":analysis.get("accuracy",0),
    "wins":analysis.get("wins",0),
    "losses":analysis.get("losses",0),
    "profit_sum":analysis.get("profit_sum",0),
    "reward":
        1 if analysis.get("accuracy",0)>50 else -1
}


reward.append(sample)

os.makedirs(
    "app/learning/data",
    exist_ok=True
)

json.dump(
    reward,
    open(memory,"w"),
    indent=2
)

print(json.dumps(sample,indent=2))
print("REWARD MEMORY UPDATED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

