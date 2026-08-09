
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="reward_feedback_$(date +%Y%m%d_%H%M%S).log"

echo "=== REWARD FEEDBACK LOOP ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

reward_file="app/learning/data/reward_memory.json"
weight_file="app/ai/memory/strategy_weights.json"

if os.path.exists(reward_file):
    try:
        rewards=json.load(open(reward_file))
    except:
        rewards=[]
else:
    rewards=[]

if not isinstance(rewards,list):
    rewards=[]

positive=0
negative=0

for r in rewards:
    if r.get("reward",0)>0:
        positive+=1
    elif r.get("reward",0)<0:
        negative+=1

total=positive+negative

score=round((positive-negative)/total*100,2) if total else 0

if score > 20:
    mode="AGGRESSIVE"
elif score < -20:
    mode="DEFENSIVE"
else:
    mode="BALANCED"


weights={
    "updated":datetime.now(timezone.utc).isoformat(),
    "positive_samples":positive,
    "negative_samples":negative,
    "learning_score":score,
    "strategy_mode":mode
}

os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    weights,
    open(weight_file,"w"),
    indent=2
)

print(json.dumps(weights,indent=2))
print("FEEDBACK LOOP UPDATED")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

