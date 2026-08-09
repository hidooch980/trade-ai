#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="exit_intelligence_$(date +%Y%m%d_%H%M%S).log"

echo "=== EXIT INTELLIGENCE BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


position_file="app/execution/live_position_state.json"
output="app/execution/exit_decision.json"


if os.path.exists(position_file):
    data=json.load(open(position_file))
else:
    data={}


positions=data.get("positions",[])

decisions=[]


for p in positions:

    if p.get("status")!="OPEN":
        continue

    entry=p.get("entry",0)
    current=p.get("current_price",0)

    profit=round(
        (current-entry)*p.get("volume",0),
        4
    )

    stop=p.get("stop_loss",None)

    if stop is not None and profit <= stop:
        action="CLOSE"
        reason="STOP_LOSS"

    elif profit > 0:
        action="HOLD"
        reason="PROFIT_PROTECTION"

    else:
        action="HOLD"
        reason="WAIT_RECOVERY"


    decisions.append({
        "ticket":p.get("ticket"),
        "symbol":p.get("symbol"),
        "profit":profit,
        "action":action,
        "reason":reason
    })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "positions_checked":len(decisions),
    "exit_decisions":decisions,
    "engine":"EXIT_INTELLIGENCE"
}


os.makedirs(
    "app/execution",
    exist_ok=True
)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("EXIT INTELLIGENCE READY")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

