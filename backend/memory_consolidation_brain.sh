#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="memory_consolidation_$(date +%Y%m%d_%H%M%S).log"

echo "=== MEMORY CONSOLIDATION BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


reward_file="app/learning/data/reward_memory.json"
output="app/ai/memory/consolidated_brain_state.json"


if os.path.exists(reward_file):
    try:
        rewards=json.load(open(reward_file))
    except:
        rewards=[]
else:
    rewards=[]


wins=sum(1 for r in rewards if r.get("reward",0)>0)
losses=sum(1 for r in rewards if r.get("reward",0)<0)

total=wins+losses

accuracy=round((wins/total)*100,2) if total else 0

score=sum(r.get("reward",0) for r in rewards)


if score > 0:
    state="LEARNING_POSITIVE"
elif score < 0:
    state="LEARNING_DEFENSIVE"
else:
    state="NEUTRAL"


brain={
    "updated":datetime.now(timezone.utc).isoformat(),
    "samples":total,
    "wins":wins,
    "losses":losses,
    "accuracy":accuracy,
    "reward_score":score,
    "brain_state":state
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    brain,
    open(output,"w"),
    indent=2
)

print(json.dumps(brain,indent=2))
print("MEMORY CONSOLIDATION COMPLETE")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

