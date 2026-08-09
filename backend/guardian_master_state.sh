#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_master_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN MASTER STATE ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
import subprocess
from datetime import datetime, timezone


output="app/execution/guardian_master_state.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


def service_status(name):
    try:
        return subprocess.check_output(
            ["systemctl","is-active",name],
            text=True
        ).strip()
    except:
        return "inactive"


health=load(
    "app/execution/guardian_health.json",
    {}
)

recovery=load(
    "app/execution/guardian_recovery_state.json",
    {}
)

risk=load(
    "app/risk/adaptive_risk_profile.json",
    {}
)

supervisor=load(
    "app/execution/live_supervisor_state.json",
    {}
)

permission=load(
    "app/execution/risk_aware_execution_permission.json",
    {}
)


result={
    "time":datetime.now(timezone.utc).isoformat(),

    "engine":"GUARDIAN_MASTER_STATE",

    "services":{
        "trade_guardian":
            service_status("trade-guardian.service"),
        "health_monitor":
            service_status("guardian-health-monitor.timer"),
        "auto_recovery":
            service_status("guardian-auto-recovery.timer")
    },

    "risk":{
        "mode":risk.get("risk_mode"),
        "level":risk.get("risk_level"),
        "multiplier":risk.get("position_multiplier")
    },

    "positions":{
        "open":supervisor.get("open_positions",0),
        "signals":supervisor.get("signals",[])
    },

    "execution":{
        "permission":permission.get("permission"),
        "action":permission.get("requested_action")
    },

    "health":health,

    "recovery":recovery,

    "status":"ONLINE"
}


os.makedirs("app/execution",exist_ok=True)


json.dump(
    result,
    open(output,"w"),
    indent=2
)


print(json.dumps(result,indent=2))
print("MASTER STATE READY")

PY

echo "REPORT:$LOG"

