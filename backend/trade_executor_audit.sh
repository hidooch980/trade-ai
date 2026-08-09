
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="trade_executor_audit_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE EXECUTOR AUDIT ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone
import uuid


safety_file="app/execution/execution_safety_status.json"
audit_file="app/execution/trade_audit_log.json"


if os.path.exists(safety_file):
    safety=json.load(open(safety_file))
else:
    safety={}


if os.path.exists(audit_file):
    try:
        audit=json.load(open(audit_file))
    except:
        audit=[]
else:
    audit=[]


if not isinstance(audit,list):
    audit=[]


if safety.get("execution")=="APPROVED":

    ticket={
        "ticket":str(uuid.uuid4()),
        "time":datetime.now(timezone.utc).isoformat(),
        "symbol":safety.get("symbol"),
        "action":safety.get("decision"),
        "status":"CREATED",
        "source":"AI_EXECUTOR"
    }

    audit.append(ticket)

    result=ticket

else:

    result={
        "status":"NOT_CREATED",
        "reason":safety.get("reason","BLOCKED")
    }


os.makedirs("app/execution",exist_ok=True)

json.dump(
    audit,
    open(audit_file,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("EXECUTOR AUDIT READY")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

