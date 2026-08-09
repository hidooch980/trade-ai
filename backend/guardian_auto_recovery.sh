#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_recovery_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN AUTO RECOVERY ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
import subprocess
from datetime import datetime, timezone


output="app/execution/guardian_recovery_state.json"


def check_service(name):
    try:
        result=subprocess.check_output(
            ["systemctl","is-active",name],
            text=True
        ).strip()
        return result
    except:
        return "inactive"


service="trade-guardian.service"

status=check_service(service)

restarted=False


if status!="active":

    subprocess.run(
        ["systemctl","restart",service]
    )

    restarted=True

    status=check_service(service)


result={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"GUARDIAN_AUTO_RECOVERY",
    "service":service,
    "status":status,
    "restarted":restarted
}


os.makedirs("app/execution",exist_ok=True)

json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("AUTO RECOVERY ACTIVE")

PY

echo "REPORT:$LOG"

