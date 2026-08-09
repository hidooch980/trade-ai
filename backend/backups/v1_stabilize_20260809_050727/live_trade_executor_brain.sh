
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="live_executor_$(date +%Y%m%d_%H%M%S).log"

echo "=== LIVE TRADE EXECUTOR BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
import uuid
from datetime import datetime, timezone


permission_file="app/execution/final_execution_permission.json"

position_file="positions.json"

audit_file="app/execution/live_trade_audit.json"


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


if permission.get("permission")=="APPROVED":

    ticket=str(uuid.uuid4())

    position={
        "ticket":ticket,
        "symbol":"BTCUSD",
        "side":"BUY",
        "volume":0.01,
        "entry":50000,
        "status":"OPEN",
        "created":datetime.now(timezone.utc).isoformat(),
        "source":"BRAIN_EXECUTOR"
    }

    positions.append(position)

    audit.append({
        "ticket":ticket,
        "event":"OPEN_POSITION",
        "time":datetime.now(timezone.utc).isoformat(),
        "status":"CREATED"
    })

    result=position

else:

    result={
        "status":"BLOCKED",
        "reason":"EXECUTION_PERMISSION_DENIED"
    }


json.dump(
    positions,
    open(position_file,"w"),
    indent=2
)

json.dump(
    audit,
    open(audit_file,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("LIVE EXECUTOR READY")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

