#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="adaptive_risk_learning_$(date +%Y%m%d_%H%M%S).log"

echo "=== ADAPTIVE RISK LEARNING BRIDGE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

analysis_file="app/ai/memory/closed_trade_analysis.json"
output="app/risk/adaptive_risk_profile.json"

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}

analysis=load(analysis_file)

wins=analysis.get("wins",0)
losses=analysis.get("losses",0)
total=wins+losses

if total:
    loss_rate=round((losses/total)*100,2)
else:
    loss_rate=0


if losses > wins:
    risk_mode="DEFENSIVE"
    risk_level="LOW"
    position_multiplier=0.5

elif wins > losses:
    risk_mode="NORMAL"
    risk_level="MEDIUM"
    position_multiplier=1.0

else:
    risk_mode="BALANCED"
    risk_level="LOW"
    position_multiplier=0.7


profile={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"ADAPTIVE_RISK_LEARNING",
    "wins":wins,
    "losses":losses,
    "loss_rate":loss_rate,
    "risk_mode":risk_mode,
    "risk_level":risk_level,
    "position_multiplier":position_multiplier,
    "status":"CONNECTED"
}


os.makedirs("app/risk",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("ADAPTIVE RISK CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

