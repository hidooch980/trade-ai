
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="close_feedback_$(date +%Y%m%d_%H%M%S).log"

echo "=== CLOSE MANAGER FEEDBACK ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


position_file="app/execution/live_position_state.json"
reward_file="app/learning/data/reward_memory.json"
output="app/execution/close_result.json"


if os.path.exists(position_file):
    data=json.load(open(position_file))
else:
    data={}


positions=data.get("positions",[])


closed=[]

for p in positions:

    if p.get("status")=="OPEN":

        entry=p.get("entry",0)
        price=p.get("current_price",0)
        volume=p.get("volume",0)

        profit=round((price-entry)*volume,4)

        result={
            "ticket":p.get("ticket"),
            "symbol":p.get("symbol"),
            "profit":profit,
            "status":"CLOSED",
            "time":datetime.now(timezone.utc).isoformat()
        }

        closed.append(result)


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
        "profit":c["profit"]
    })


os.makedirs("app/execution",exist_ok=True)

json.dump(
    closed,
    open(output,"w"),
    indent=2
)


json.dump(
    rewards,
    open(reward_file,"w"),
    indent=2
)


print(json.dumps(closed,indent=2))
print("CLOSE FEEDBACK UPDATED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

