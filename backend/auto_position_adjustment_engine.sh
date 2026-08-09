#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="position_adjustment_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTO POSITION ADJUSTMENT ENGINE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


response_file="app/execution/guardian_auto_response.json"
position_file="positions.json"

output="app/execution/position_adjustment_state.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


response=load(response_file,{})
positions=load(position_file,[])


if not isinstance(positions,list):
    positions=[]


actions=response.get("responses",[])

action_map={}

for a in actions:
    action_map[a.get("ticket")]=a.get("action")


adjusted=[]


for p in positions:

    if p.get("status")!="OPEN":
        continue

    ticket=p.get("ticket")

    action=action_map.get(ticket,"MONITOR")

    old_volume=p.get("volume",0)

    if action=="FORCE_REDUCE":

        new_volume=round(old_volume*0.5,4)
        p["volume"]=new_volume
        status="REDUCED"


    elif action=="PREPARE_CLOSE":

        new_volume=old_volume
        status="CLOSE_READY"


    else:

        new_volume=old_volume
        status="UNCHANGED"


    adjusted.append({
        "ticket":ticket,
        "symbol":p.get("symbol"),
        "old_volume":old_volume,
        "new_volume":new_volume,
        "action":action,
        "status":status
    })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"AUTO_POSITION_ADJUSTMENT",
    "adjusted_positions":len(adjusted),
    "positions":adjusted,
    "status":"ACTIVE"
}


os.makedirs("app/execution",exist_ok=True)


json.dump(
    positions,
    open(position_file,"w"),
    indent=2
)


json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("POSITION ADJUSTMENT COMPLETE")


PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

