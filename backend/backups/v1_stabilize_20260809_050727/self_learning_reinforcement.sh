
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="self_learning_$(date +%Y%m%d_%H%M%S).log"

echo "=== SELF LEARNING REINFORCEMENT ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


reward_file="app/learning/data/reward_memory.json"
output="app/ai/memory/reinforcement_weights.json"


if os.path.exists(reward_file):
    try:
        rewards=json.load(open(reward_file))
    except:
        rewards=[]
else:
    rewards=[]


if not isinstance(rewards,list):
    rewards=[]


wins=0
losses=0
total_reward=0


for r in rewards:

    value=r.get("reward",0)

    total_reward += value

    if value > 0:
        wins += 1
    elif value < 0:
        losses += 1


samples=wins+losses

accuracy=round((wins/samples)*100,2) if samples else 0


if total_reward > 0:
    mode="IMPROVING"
    confidence=min(100,50+total_reward*5)

elif total_reward < 0:
    mode="CAUTION"
    confidence=max(0,50+total_reward*5)

else:
    mode="NEUTRAL"
    confidence=50


result={
    "updated":datetime.now(timezone.utc).isoformat(),
    "samples":samples,
    "wins":wins,
    "losses":losses,
    "accuracy":accuracy,
    "total_reward":total_reward,
    "learning_mode":mode,
    "confidence":confidence
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("REINFORCEMENT COMPLETE")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

