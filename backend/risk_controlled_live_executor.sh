#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="risk_executor_$(date +%Y%m%d_%H%M%S).log"

echo "=== RISK CONTROLLED LIVE EXECUTOR ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
import uuid
from datetime import datetime, timezone

permission_file="app/execution/risk_aware_execution_permission.json"
position_file="positions.json"
audit_file="app/execution/risk_controlled_audit.json"

def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


permission=load(permission_file,{})
positions=load(position_file,[])
audit=load(audit_file,[])

if not isinstance(positions,list):
    positions=[]

if not isinstance(audit,list):
    audit=[]


if permission.get("permission")=="APPROVED_WITH_LIMIT":

    multiplier=permission.get("position_multiplier",0.5)

    base_volume=0.01
    volume=round(base_volume*multiplier,4)

    ticket=str(uuid.uuid4())

    position={
        "ticket":ticket,
        "symbol":"BTCUSD",
        "side":"BUY",
        "volume":volume,
        "risk_multiplier":multiplier,
        "status":"OPEN",
        "created":datetime.now(timezone.utc).isoformat(),
        "source":"RISK_CONTROLLED_EXECUTOR"
    }

    positions.append(position)

    audit.append({
        "ticket":ticket,
        "event":"OPEN_RISK_CONTROLLED_POSITION",
        "volume":volume,
        "time":datetime.now(timezone.utc).isoformat()
    })

    result=position

else:

    result={
        "status":"BLOCKED",
        "reason":"RISK_GATE_NOT_APPROVED"
    }


json.dump(
    positions,
    open(position_file,"w"),
    indent=2
)

os.makedirs("app/execution",exist_ok=True)

json.dump(
    audit,
    open(audit_file,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("RISK CONTROLLED EXECUTOR READY")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

