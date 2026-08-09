
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="final_decision_connector_$(date +%Y%m%d_%H%M%S).log"

echo "=== FINAL DECISION CONNECTOR ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

risk_file="app/risk/risk_gate_status.json"

if os.path.exists(risk_file):
    risk=json.load(open(risk_file))
else:
    risk={}


signal={
    "symbol":"BTCUSD",
    "direction":"BUY",
    "indicator_score":80,
    "ai_score":85,
    "smart_money_score":80,
    "confidence":85
}


if risk.get("decision")!="ALLOW":

    result={
        "decision":"BLOCK",
        "reason":"RISK_GATE_BLOCK"
    }

else:

    score=(
        signal["indicator_score"]+
        signal["ai_score"]+
        signal["smart_money_score"]
    )/3

    if score>=70 and signal["confidence"]>=70:
        decision="BUY"
    else:
        decision="WAIT"


    result={
        "time":datetime.now(timezone.utc).isoformat(),
        "decision":decision,
        "score":score,
        "risk_gate":risk.get("decision"),
        "confidence":signal["confidence"]
    }


os.makedirs("app/decision",exist_ok=True)

json.dump(
    result,
    open("app/decision/final_connector_test.json","w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("FINAL DECISION CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

