#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_response_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN AUTO RESPONSE ENGINE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

guardian_file="app/execution/position_guardian_v2_state.json"
output="app/execution/guardian_auto_response.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


guardian=load(guardian_file,{})

positions=guardian.get("positions",[])

responses=[]


for p in positions:

    ticket=p.get("ticket")
    pnl=p.get("pnl",0)
    drawdown=p.get("drawdown_percent",0)

    if drawdown <= -5:
        action="PREPARE_CLOSE"

    elif pnl < -100:
        action="FORCE_REDUCE"

    else:
        action="MONITOR"


    responses.append({
        "ticket":ticket,
        "symbol":p.get("symbol"),
        "pnl":pnl,
        "drawdown":drawdown,
        "action":action
    })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"GUARDIAN_AUTO_RESPONSE",
    "responses":responses,
    "status":"ACTIVE"
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("GUARDIAN RESPONSE READY")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

