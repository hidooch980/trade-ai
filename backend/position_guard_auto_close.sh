#!/bin/bash

cd /opt/trade-ai/backend || exit 1

echo "=== POSITION GUARD AUTO CLOSE ==="

./venv/bin/python - <<'PY'

import json
import os
from datetime import datetime, timezone

position_file="positions.json"
output="app/execution/position_guard_status.json"

if os.path.exists(position_file):
    positions=json.load(open(position_file))
else:
    positions=[]

symbols={}
duplicates=[]
close_candidates=[]

for p in positions:
    if p.get("status")=="OPEN":

        symbol=p.get("symbol")

        if symbol in symbols:
            duplicates.append(p.get("ticket"))
        else:
            symbols[symbol]=p.get("ticket")

        entry=p.get("entry_price",0)
        current=p.get("current_price",entry)
        volume=p.get("volume",0)

        pnl=round((current-entry)*volume,4)

        if pnl < -100:
            close_candidates.append({
                "ticket":p.get("ticket"),
                "symbol":symbol,
                "pnl":pnl,
                "action":"CLOSE"
            })


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"POSITION_GUARD_AUTO_CLOSE",
    "open_positions":len(symbols),
    "duplicate_positions":duplicates,
    "close_candidates":close_candidates,
    "status":"READY"
}

os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))

PY

curl -s http://127.0.0.1:8000/health

