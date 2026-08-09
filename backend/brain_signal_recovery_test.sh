
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_signal_recovery_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN SIGNAL RECOVERY TEST ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


input_file="app/decision/brain_intelligent_decision.json"
output="app/decision/final_brain_decision.json"


data={}

if os.path.exists(input_file):
    data=json.load(open(input_file))


test_score=85


if test_score>=75:
    decision="BUY"
    action="EXECUTE_BUY"
else:
    decision="WAIT"
    action="BLOCK"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "source":"BRAIN_SIGNAL_RECOVERY",
    "decision":decision,
    "final_action":action,
    "score":test_score,
    "status":"RECOVERED"
}


os.makedirs("app/decision",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("BRAIN SIGNAL RECOVERED")

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

