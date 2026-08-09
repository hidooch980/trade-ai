
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="execution_safety_$(date +%Y%m%d_%H%M%S).log"

echo "=== EXECUTION SAFETY LAYER ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

decision_file="app/decision/final_connector_test.json"
position_file="positions.json"
output="app/execution/execution_safety_status.json"


if os.path.exists(decision_file):
    decision=json.load(open(decision_file))
else:
    decision={}


if os.path.exists(position_file):
    try:
        positions=json.load(open(position_file))
    except:
        positions=[]
else:
    positions=[]


symbol=decision.get("symbol","BTCUSD")
action=decision.get("decision","WAIT")


existing=False

if isinstance(positions,list):
    for p in positions:
        if p.get("symbol")==symbol:
            existing=True


if action=="BUY" and not existing:
    execution="APPROVED"
    reason="NO_DUPLICATE_POSITION"
elif existing:
    execution="BLOCKED"
    reason="POSITION_EXISTS"
else:
    execution="WAIT"
    reason="NO_TRADE_SIGNAL"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "execution":execution,
    "reason":reason,
    "symbol":symbol,
    "decision":action
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("EXECUTION SAFETY READY")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

