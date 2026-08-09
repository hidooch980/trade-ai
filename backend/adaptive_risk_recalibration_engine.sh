#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="risk_recalibration_$(date +%Y%m%d_%H%M%S).log"

echo "=== ADAPTIVE RISK RECALIBRATION ENGINE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

feedback_file="app/ai/memory/reward_feedback_state.json"
output="app/risk/adaptive_risk_profile.json"

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}

feedback=load(feedback_file)

wins=feedback.get("wins",0)
losses=feedback.get("losses",0)

if losses > wins:
    mode="DEFENSIVE"
    level="LOW"
    multiplier=0.5

elif wins > losses:
    mode="NORMAL"
    level="MEDIUM"
    multiplier=1.0

else:
    mode="BALANCED"
    level="LOW"
    multiplier=0.7


profile={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"ADAPTIVE_RISK_RECALIBRATION",
    "wins":wins,
    "losses":losses,
    "risk_mode":mode,
    "risk_level":level,
    "position_multiplier":multiplier,
    "status":"UPDATED"
}


os.makedirs("app/risk",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("RISK PROFILE RECALIBRATED")

PY

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

