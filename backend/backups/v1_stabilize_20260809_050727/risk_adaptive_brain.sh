
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="risk_adaptive_$(date +%Y%m%d_%H%M%S).log"

echo "=== RISK ADAPTIVE BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

weight_file="app/ai/memory/strategy_weights.json"
output="app/risk/adaptive_risk_profile.json"

if os.path.exists(weight_file):
    try:
        data=json.load(open(weight_file))
    except:
        data={}
else:
    data={}


score=data.get("learning_score",0)
mode=data.get("strategy_mode","BALANCED")


if score < -20:
    risk_level="LOW"
    max_risk=0.5

elif score > 20 and mode=="AGGRESSIVE":
    risk_level="MEDIUM"
    max_risk=1.5

else:
    risk_level="NORMAL"
    max_risk=1.0


profile={
    "updated":datetime.now(timezone.utc).isoformat(),
    "learning_score":score,
    "strategy_mode":mode,
    "risk_level":risk_level,
    "max_risk_percent":max_risk,
    "trade_allowed": True
}


os.makedirs("app/risk",exist_ok=True)

json.dump(
    profile,
    open(output,"w"),
    indent=2
)

print(json.dumps(profile,indent=2))
print("RISK PROFILE UPDATED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

