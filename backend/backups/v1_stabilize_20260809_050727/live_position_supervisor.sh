#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="live_position_supervisor_$(date +%Y%m%d_%H%M%S).log"

echo "=== LIVE POSITION SUPERVISOR ===" | tee -a "$LOG"

./venv/bin/python - <<'PY' | tee -a "$LOG"

import json
import os
from datetime import datetime, timezone

position_file = "positions.json"
output = "app/execution/live_supervisor_state.json"


def load(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return default
    return default


positions = load(position_file, [])

if not isinstance(positions, list):
    positions = []

signals = []

for p in positions:

    if p.get("status") != "OPEN":
        continue

    ticket = p.get("ticket")
    symbol = p.get("symbol")
    side = str(p.get("side", "BUY")).upper()

    entry = float(p.get("entry_price", 0) or 0)
    current = float(p.get("current_price", entry) or entry)
    volume = float(p.get("volume", 0) or 0)

    # Correct directional PnL
    if side == "SELL":
        pnl = round((entry - current) * volume, 4)
    else:
        pnl = round((current - entry) * volume, 4)

    # Correct directional drawdown from entry
    if entry:
        if side == "SELL":
            drawdown = round(((entry - current) / entry) * 100, 4)
        else:
            drawdown = round(((current - entry) / entry) * 100, 4)
    else:
        drawdown = 0

    if drawdown <= -5:
        action = "PREPARE_CLOSE"
    elif pnl < -100:
        action = "FORCE_REDUCE"
    else:
        action = "MONITOR"

    signals.append({
        "ticket": ticket,
        "symbol": symbol,
        "side": side,
        "pnl": pnl,
        "drawdown": drawdown,
        "action": action
    })


result = {
    "time": datetime.now(timezone.utc).isoformat(),
    "engine": "LIVE_POSITION_SUPERVISOR",
    "open_positions": len(signals),
    "signals": signals,
    "status": "RUNNING"
}

os.makedirs("app/execution", exist_ok=True)

with open(output, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
print("LIVE SUPERVISOR ACTIVE")

PY

curl -s http://127.0.0.1:8000/health | tee -a "$LOG"
echo "REPORT:$LOG"
