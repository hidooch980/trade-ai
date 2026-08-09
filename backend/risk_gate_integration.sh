
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="risk_gate_$(date +%Y%m%d_%H%M%S).log"

echo "=== RISK GATE INTEGRATION ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

profile_file="app/risk/adaptive_risk_profile.json"
output="app/risk/risk_gate_status.json"

if os.path.exists(profile_file):
    try:
        profile=json.load(open(profile_file))
    except:
        profile={}
else:
    profile={}


allowed=profile.get("trade_allowed",False)
level=profile.get("risk_level","UNKNOWN")
max_risk=profile.get("max_risk_percent",0)


if allowed and max_risk > 0:
    decision="ALLOW"
    reason="RISK_PROFILE_ACCEPTED"
else:
    decision="BLOCK"
    reason="RISK_LIMIT_REJECTED"


gate={
    "time":datetime.now(timezone.utc).isoformat(),
    "decision":decision,
    "reason":reason,
    "risk_level":level,
    "max_risk_percent":max_risk
}


os.makedirs("app/risk",exist_ok=True)

json.dump(
    gate,
    open(output,"w"),
    indent=2
)


print(json.dumps(gate,indent=2))
print("RISK GATE READY")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

