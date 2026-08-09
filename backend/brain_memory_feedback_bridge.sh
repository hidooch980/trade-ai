#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_memory_bridge_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN MEMORY FEEDBACK BRIDGE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

memory_file="app/ai/memory/consolidated_brain_state.json"
strategy_file="app/ai/memory/optimized_strategy.json"
output="app/ai/memory/brain_feedback_profile.json"

memory={}
strategy={}

if os.path.exists(memory_file):
    memory=json.load(open(memory_file))

if os.path.exists(strategy_file):
    strategy=json.load(open(strategy_file))


accuracy=memory.get("accuracy",0)
reward=memory.get("reward_score",0)
state=memory.get("brain_state","UNKNOWN")

confidence=strategy.get("confidence",50)


if reward > 0 and accuracy >= 55:
    feedback="POSITIVE_LEARNING"
    adjustment="INCREASE_TRUST"

elif reward < 0:
    feedback="NEGATIVE_LEARNING"
    adjustment="REDUCE_RISK"

else:
    feedback="NEUTRAL"
    adjustment="KEEP"


profile={
    "time":datetime.now(timezone.utc).isoformat(),
    "memory_state":state,
    "accuracy":accuracy,
    "reward_score":reward,
    "previous_confidence":confidence,
    "feedback":feedback,
    "adjustment":adjustment,
    "bridge":"CONNECTED"
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("BRAIN MEMORY FEEDBACK CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

