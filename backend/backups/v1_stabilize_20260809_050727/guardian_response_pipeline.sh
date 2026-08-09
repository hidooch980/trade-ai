#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_pipeline_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN RESPONSE PIPELINE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

response_file="app/execution/guardian_auto_response.json"
adjust_output="app/execution/guardian_pipeline_action.json"

def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


response=load(response_file,{})

responses=response.get("responses",[])

actions=[]

for r in responses:

    ticket=r.get("ticket")
    action=r.get("action")

    if action=="FORCE_REDUCE":
        next_action="REDUCE_POSITION"

    elif action=="PREPARE_CLOSE":
        next_action="CLOSE_POSITION"

    else:
        next_action="KEEP_MONITORING"


    actions.append({
        "ticket":ticket,
        "symbol":r.get("symbol"),
        "guardian_action":action,
        "pipeline_action":next_action
    })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"GUARDIAN_RESPONSE_PIPELINE",
    "signals_received":len(responses),
    "actions":actions,
    "status":"CONNECTED"
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(adjust_output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("GUARDIAN PIPELINE CONNECTED")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

