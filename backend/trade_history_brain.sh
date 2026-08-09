#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="trade_history_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE HISTORY BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

position_file="positions.json"
output="app/ai/memory/trade_history.json"

if os.path.exists(position_file):
    positions=json.load(open(position_file))
else:
    positions=[]

history=[]

for p in positions:

    if p.get("status")=="CLOSED":

        pnl=p.get("pnl",p.get("profit",0))

        if pnl > 0:
            result="WIN"
        elif pnl < 0:
            result="LOSS"
        else:
            result="BREAKEVEN"

        history.append({
            "ticket":p.get("ticket"),
            "symbol":p.get("symbol"),
            "side":p.get("side"),
            "pnl":pnl,
            "result":result,
            "close_reason":p.get("close_reason"),
            "time":p.get("close_time")
        })


summary={
    "updated":datetime.now(timezone.utc).isoformat(),
    "total_closed":len(history),
    "wins":sum(1 for x in history if x["result"]=="WIN"),
    "losses":sum(1 for x in history if x["result"]=="LOSS"),
    "breakeven":sum(1 for x in history if x["result"]=="BREAKEVEN"),
    "trades":history
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    summary,
    open(output,"w"),
    indent=2
)

print(json.dumps(summary,indent=2))
print("TRADE HISTORY READY")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

