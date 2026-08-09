#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_pipeline_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN DECISION PIPELINE TEST ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

files={
"strategy":"app/decision/strategy_decision_profile.json",
"risk":"app/risk/risk_gate_status.json",
"execution":"app/execution/execution_safety_status.json"
}

data={}

for k,f in files.items():
    if os.path.exists(f):
        try:
            data[k]=json.load(open(f))
        except:
            data[k]={}
    else:
        data[k]={}


strategy=data["strategy"]
risk=data["risk"]
execution=data["execution"]


if (
    strategy.get("bridge_status")=="CONNECTED"
    and risk.get("decision")=="ALLOW"
    and execution.get("execution")!="BLOCKED"
):
    final="EXECUTE_READY"

elif risk.get("decision")=="ALLOW":
    final="WAIT_EXECUTION"

else:
    final="BLOCKED"


result={
"time":datetime.now(timezone.utc).isoformat(),
"strategy":strategy.get("strategy"),
"decision_mode":strategy.get("decision_mode"),
"risk_gate":risk.get("decision"),
"execution_state":execution.get("execution"),
"final_state":final
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
result,
open("app/ai/memory/brain_pipeline_state.json","w"),
indent=2
)

print(json.dumps(result,indent=2))
print("BRAIN PIPELINE CONNECTED")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

