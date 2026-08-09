#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="final_ai_bridge_$(date +%Y%m%d_%H%M%S).log"

echo "=== FINAL AI DECISION BRIDGE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


strategy_file="app/decision/strategy_decision_profile.json"
risk_file="app/risk/risk_gate_status.json"

output="app/decision/final_ai_decision.json"


def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}


strategy=load(strategy_file)
risk=load(risk_file)


decision_mode=strategy.get(
    "decision_mode",
    "SAFE_MODE"
)

confidence=strategy.get(
    "confidence",
    0
)

risk_gate=risk.get(
    "decision",
    "BLOCK"
)


signal_score=(
    80 +
    85 +
    80
)/3


if risk_gate!="ALLOW":

    decision="BLOCK"
    reason="RISK_GATE"


elif decision_mode=="STRICT_FILTER":

    if confidence>=60 and signal_score>=75:
        decision="BUY"
        reason="STRICT_FILTER_ACCEPTED"
    else:
        decision="WAIT"
        reason="CONFIDENCE_LOW"


elif decision_mode=="NORMAL_EXECUTION":

    decision="BUY"
    reason="NORMAL_STRATEGY"


else:

    decision="WAIT"
    reason="SAFE_MODE"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "decision":decision,
    "reason":reason,
    "score":signal_score,
    "confidence":confidence,
    "strategy_mode":decision_mode,
    "risk_gate":risk_gate
}


os.makedirs(
    "app/decision",
    exist_ok=True
)


json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("FINAL AI BRIDGE READY")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

