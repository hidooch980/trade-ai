from fastapi import APIRouter
import json
import os
from datetime import datetime, timezone

router = APIRouter()

STATE_FILE = "app/execution/guardian_master_state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass

    return {
        "status": "NO_STATE",
        "time": datetime.now(timezone.utc).isoformat()
    }


@router.get("/guardian/status")
def guardian_status():
    return load_state()


@router.get("/guardian/summary")
def guardian_summary():
    state = load_state()

    return {
        "status": state.get("status"),
        "services": state.get("services"),
        "risk": state.get("risk"),
        "open_positions": state.get("positions", {}).get("open"),
        "execution": state.get("execution")
    }
