#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="supervisor_guardian_sync_$(date +%Y%m%d_%H%M%S).log"

echo "=== SUPERVISOR GUARDIAN SYNC ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


supervisor_file="app/execution/live_supervisor_state.json"
output="app/execution/guardian_auto_response.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


supervisor=load(supervisor_file,{})

signals=supervisor.get("signals",[])

responses=[]


for s in signals:

    action=s.get("action","MONITOR")

    if action=="FORCE_REDUCE":
        response="FORCE_REDUCE"

    elif action=="PREPARE_CLOSE":
        response="PREPARE_CLOSE"

    else:
        response="MONITOR"


    responses.append({
        "ticket":s.get("ticket"),
        "symbol":s.get("symbol"),
        "pnl":s.get("pnl"),
        "drawdown":s.get("drawdown"),
        "action":response
    })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"SUPERVISOR_GUARDIAN_SYNC",
    "responses":responses,
    "status":"CONNECTED"
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("SUPERVISOR CONNECTED TO GUARDIAN")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

