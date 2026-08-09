#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="auto_close_executor_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTO CLOSE EXECUTOR BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


guard_file="app/execution/position_guard_status.json"
position_file="positions.json"
reward_file="app/learning/data/reward_memory.json"
output="app/execution/auto_close_result.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


guard=load(guard_file,{})
positions=load(position_file,[])
rewards=load(reward_file,[])


if not isinstance(positions,list):
    positions=[]

if not isinstance(rewards,list):
    rewards=[]


close_map={}

for c in guard.get("close_candidates",[]):
    close_map[c.get("ticket")]=c


closed=[]


for p in positions:

    ticket=p.get("ticket")

    if ticket in close_map and p.get("status")=="OPEN":

        pnl=close_map[ticket].get("pnl",0)

        p["status"]="CLOSED"
        p["close_time"]=datetime.now(timezone.utc).isoformat()
        p["close_reason"]="AUTO_CLOSE_BRAIN"

        closed.append({
            "ticket":ticket,
            "symbol":p.get("symbol"),
            "pnl":pnl,
            "status":"CLOSED"
        })

        rewards.append({
            "time":datetime.now(timezone.utc).isoformat(),
            "reward":1 if pnl>0 else -1,
            "profit":pnl,
            "source":"AUTO_CLOSE_EXECUTOR"
        })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"AUTO_CLOSE_EXECUTOR_BRAIN",
    "closed_positions":len(closed),
    "closed":closed,
    "learning_sync":"UPDATED"
}


os.makedirs("app/execution",exist_ok=True)
os.makedirs("app/learning/data",exist_ok=True)


json.dump(
    positions,
    open(position_file,"w"),
    indent=2
)

json.dump(
    rewards,
    open(reward_file,"w"),
    indent=2
)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

