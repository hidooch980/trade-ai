#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_health_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN HEALTH MONITOR ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone

service="trade-guardian.service"

output="app/execution/guardian_health.json"


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"GUARDIAN_HEALTH_MONITOR",
    "service":service,
    "status":"CHECKED"
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)

print(json.dumps(result,indent=2))
print("HEALTH MONITOR ACTIVE")

PY

systemctl is-active trade-guardian.service | tee -a $LOG

echo "REPORT:$LOG"

