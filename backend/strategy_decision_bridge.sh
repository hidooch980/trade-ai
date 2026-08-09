#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="strategy_bridge_$(date +%Y%m%d_%H%M%S).log"

echo "=== STRATEGY DECISION BRIDGE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

strategy_file="app/ai/memory/optimized_strategy.json"
output="app/decision/strategy_decision_profile.json"

if os.path.exists(strategy_file):
    strategy=json.load(open(strategy_file))
else:
    strategy={}

selected=strategy.get("selected_strategy","UNKNOWN")
risk=strategy.get("risk_bias","MINIMAL")
confidence=strategy.get("confidence",0)

if selected=="BALANCED_PLUS":
    decision_mode="NORMAL_EXECUTION"

elif selected=="CAUTIOUS_ADAPTIVE":
    decision_mode="STRICT_FILTER"

else:
    decision_mode="SAFE_MODE"


profile={
    "time":datetime.now(timezone.utc).isoformat(),
    "strategy":selected,
    "decision_mode":decision_mode,
    "risk_bias":risk,
    "confidence":confidence,
    "bridge_status":"CONNECTED"
}


os.makedirs("app/decision",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("STRATEGY BRIDGE CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

