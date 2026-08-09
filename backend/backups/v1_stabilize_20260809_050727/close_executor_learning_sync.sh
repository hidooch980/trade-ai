#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="close_executor_sync_$(date +%Y%m%d_%H%M%S).log"

echo "=== CLOSE EXECUTOR LEARNING SYNC ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


exit_file="app/execution/exit_decision.json"
reward_file="app/learning/data/reward_memory.json"
output="app/execution/close_execution_result.json"


if os.path.exists(exit_file):
    data=json.load(open(exit_file))
else:
    data={}


decisions=data.get("exit_decisions",[])

closed=[]


for d in decisions:

    if d.get("action")=="CLOSE":

        closed.append({
            "ticket":d.get("ticket"),
            "symbol":d.get("symbol"),
            "profit":d.get("profit"),
            "status":"CLOSED",
            "reason":d.get("reason"),
            "time":datetime.now(timezone.utc).isoformat()
        })


if os.path.exists(reward_file):
    try:
        rewards=json.load(open(reward_file))
    except:
        rewards=[]
else:
    rewards=[]


if not isinstance(rewards,list):
    rewards=[]


for c in closed:
    rewards.append({
        "time":c["time"],
        "reward":1 if c["profit"]>0 else -1,
        "profit":c["profit"],
        "source":"CLOSE_EXECUTOR"
    })


os.makedirs("app/execution",exist_ok=True)

json.dump(closed,open(output,"w"),indent=2)

json.dump(rewards,open(reward_file,"w"),indent=2)


print(json.dumps(closed,indent=2))
print("CLOSE EXECUTION SYNC COMPLETE")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

