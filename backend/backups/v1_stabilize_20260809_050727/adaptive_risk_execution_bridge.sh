#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="adaptive_risk_execution_$(date +%Y%m%d_%H%M%S).log"

echo "=== ADAPTIVE RISK EXECUTION BRIDGE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

risk_file="app/risk/adaptive_risk_profile.json"
execution_file="app/execution/final_execution_permission.json"
output="app/execution/risk_execution_profile.json"

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}

risk=load(risk_file)
execution=load(execution_file)

risk_mode=risk.get("risk_mode","UNKNOWN")
multiplier=risk.get("position_multiplier",1)

permission=execution.get("permission","WAIT")

if risk_mode=="DEFENSIVE":
    action="REDUCE_SIZE"
elif risk_mode=="BALANCED":
    action="NORMAL_SIZE"
else:
    action="FULL_SIZE"


if permission=="APPROVED":
    status="READY_WITH_RISK_CONTROL"
else:
    status="WAITING"


profile={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"ADAPTIVE_RISK_EXECUTION_BRIDGE",
    "risk_mode":risk_mode,
    "position_multiplier":multiplier,
    "risk_action":action,
    "execution_permission":permission,
    "status":status
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("ADAPTIVE RISK EXECUTION CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

