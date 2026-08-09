
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="position_lifecycle_$(date +%Y%m%d_%H%M%S).log"

echo "=== POSITION LIFECYCLE MONITOR ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


position_file="positions.json"
output="app/execution/position_lifecycle_state.json"


if os.path.exists(position_file):
    positions=json.load(open(position_file))
else:
    positions=[]


monitor=[]


for p in positions:

    if p.get("status")=="OPEN":

        entry=p.get("entry",0)
        current=p.get("current_price",entry)

        volume=p.get("volume",0)

        pnl=round((current-entry)*volume,4)

        monitor.append({
            "ticket":p.get("ticket"),
            "symbol":p.get("symbol"),
            "side":p.get("side"),
            "entry":entry,
            "current":current,
            "pnl":pnl,
            "status":"MONITORED",
            "time":datetime.now(timezone.utc).isoformat()
        })


result={
    "engine":"POSITION_LIFECYCLE_MONITOR",
    "open_positions":len(monitor),
    "positions":monitor
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("POSITION MONITOR READY")


PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

