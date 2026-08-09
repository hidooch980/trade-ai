#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="risk_aware_gate_$(date +%Y%m%d_%H%M%S).log"

echo "=== RISK AWARE EXECUTION GATE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

risk_file="app/risk/adaptive_risk_profile.json"
decision_file="app/decision/final_brain_decision.json"

output="app/execution/risk_aware_execution_permission.json"

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}

risk=load(risk_file)
decision=load(decision_file)

risk_mode=risk.get("risk_mode","UNKNOWN")
multiplier=risk.get("position_multiplier",1)

action=decision.get("final_action","BLOCK")

if risk_mode=="DEFENSIVE":
    allowed_size="REDUCED"
elif risk_mode=="NORMAL":
    allowed_size="FULL"
else:
    allowed_size="MEDIUM"


if action.startswith("EXECUTE"):
    permission="APPROVED_WITH_LIMIT"
else:
    permission="WAIT"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"RISK_AWARE_EXECUTION_GATE",
    "requested_action":action,
    "risk_mode":risk_mode,
    "position_multiplier":multiplier,
    "allowed_size":allowed_size,
    "permission":permission
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("RISK AWARE GATE CONNECTED")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

