
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="final_execution_gate_$(date +%Y%m%d_%H%M%S).log"

echo "=== FINAL EXECUTION GATE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


decision_file="app/decision/final_brain_decision.json"
risk_file="app/risk/risk_gate_status.json"

output="app/execution/final_execution_permission.json"


def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return {}
    return {}


decision=load(decision_file)
risk=load(risk_file)


action=decision.get("final_action","BLOCK")
risk_gate=risk.get("decision","BLOCK")


if action.startswith("EXECUTE") and risk_gate=="ALLOW":

    permission="APPROVED"
    reason="FINAL_CHECK_PASSED"

elif risk_gate!="ALLOW":

    permission="BLOCKED"
    reason="RISK_GATE_DENIED"

else:

    permission="WAIT"
    reason="NO_EXECUTION_SIGNAL"


result={

    "time":datetime.now(timezone.utc).isoformat(),
    "permission":permission,
    "reason":reason,
    "requested_action":action,
    "risk_gate":risk_gate,
    "engine":"FINAL_EXECUTION_GATE"

}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("FINAL EXECUTION GATE READY")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

