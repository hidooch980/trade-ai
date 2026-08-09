#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="adaptive_strategy_$(date +%Y%m%d_%H%M%S).log"

echo "=== ADAPTIVE STRATEGY BRAIN ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

reward_file="app/learning/data/reward_memory.json"
output="app/ai/memory/adaptive_strategy_weights.json"

if os.path.exists(reward_file):
    try:
        rewards=json.load(open(reward_file))
    except:
        rewards=[]
else:
    rewards=[]

if not isinstance(rewards,list):
    rewards=[]

total=0
count=0

for r in rewards:
    total += r.get("reward",0)
    count += 1

avg = round(total / count,3) if count else 0


if avg > 0:
    status="POSITIVE"
    confidence=min(100,50+avg*10)
elif avg < 0:
    status="NEGATIVE"
    confidence=max(0,50+avg*10)
else:
    status="NEUTRAL"
    confidence=50


result={
    "updated":datetime.utcnow().isoformat(),
    "reward_samples":count,
    "average_reward":avg,
    "strategy_status":status,
    "adaptive_confidence":confidence
}


os.makedirs(os.path.dirname(output),exist_ok=True)

json.dump(result,open(output,"w"),indent=2)

print(json.dumps(result,indent=2))
print("ADAPTIVE MEMORY UPDATED")

PY


echo "=== FILE CHECK ===" | tee -a $LOG
cat app/ai/memory/adaptive_strategy_weights.json | tee -a $LOG


echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "REPORT:$LOG"

