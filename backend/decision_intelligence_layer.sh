
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="decision_intelligence_$(date +%Y%m%d_%H%M%S).log"

echo "=== DECISION INTELLIGENCE LAYER ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


feedback_file="app/ai/memory/brain_feedback_profile.json"
strategy_file="app/decision/strategy_decision_profile.json"
risk_file="app/risk/risk_gate_status.json"

output="app/decision/brain_intelligent_decision.json"


def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}


feedback=load(feedback_file)
strategy=load(strategy_file)
risk=load(risk_file)


score=70

adjustment=feedback.get("adjustment")

if adjustment=="INCREASE_TRUST":
    score += 10

elif adjustment=="REDUCE_RISK":
    score -= 15


if risk.get("decision")!="ALLOW":
    decision="BLOCK"

elif score>=75:
    decision="BUY"

elif score<=40:
    decision="WAIT"

else:
    decision="FILTERED"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"BRAIN_INTELLIGENCE_LAYER",
    "base_score":70,
    "final_score":score,
    "decision":decision,
    "memory_feedback":feedback.get("feedback"),
    "strategy_mode":strategy.get("decision_mode"),
    "risk_gate":risk.get("decision")
}


os.makedirs("app/decision",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("DECISION INTELLIGENCE READY")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

