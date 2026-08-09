#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="reward_feedback_$(date +%Y%m%d_%H%M%S).log"

echo "=== REWARD FEEDBACK REINFORCEMENT ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

close_file="app/execution/auto_close_result.json"
reward_file="app/learning/data/reward_memory.json"
output="app/ai/memory/reward_feedback_state.json"

def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


close_data=load(close_file,{})
rewards=load(reward_file,[])

if not isinstance(rewards,list):
    rewards=[]


closed=close_data.get("closed",[])

for trade in closed:
    pnl=trade.get("pnl",0)

    rewards.append({
        "time":datetime.now(timezone.utc).isoformat(),
        "reward":1 if pnl>0 else -1,
        "profit":pnl,
        "source":"REWARD_FEEDBACK_ENGINE"
    })


wins=sum(1 for r in rewards if r.get("reward",0)>0)
losses=sum(1 for r in rewards if r.get("reward",0)<0)

state="NORMAL"

if losses>wins:
    state="DEFENSIVE"

result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"REWARD_FEEDBACK_REINFORCEMENT",
    "wins":wins,
    "losses":losses,
    "learning_state":state,
    "updated_rewards":len(rewards)
}


os.makedirs("app/ai/memory",exist_ok=True)
os.makedirs("app/learning/data",exist_ok=True)

json.dump(rewards,open(reward_file,"w"),indent=2)
json.dump(result,open(output,"w"),indent=2)

print(json.dumps(result,indent=2))
print("REWARD FEEDBACK COMPLETE")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

