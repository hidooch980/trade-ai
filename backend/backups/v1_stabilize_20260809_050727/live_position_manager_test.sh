
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="position_manager_$(date +%Y%m%d_%H%M%S).log"

echo "=== LIVE POSITION MANAGER ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone
import uuid


output="app/execution/live_position_state.json"

position_file="positions.json"


if os.path.exists(position_file):
    try:
        positions=json.load(open(position_file))
    except:
        positions=[]
else:
    positions=[]


if not isinstance(positions,list):
    positions=[]


state={
    "time":datetime.now(timezone.utc).isoformat(),
    "open_positions":len(positions),
    "positions":positions,
    "manager_status":"ACTIVE"
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    state,
    open(output,"w"),
    indent=2
)


print(json.dumps(state,indent=2))
print("POSITION MANAGER READY")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

