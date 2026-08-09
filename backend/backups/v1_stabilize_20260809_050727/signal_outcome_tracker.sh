#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="signal_outcome_$(date +%Y%m%d_%H%M%S).log"

echo "=== SIGNAL OUTCOME TRACKER ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

signals_file="app/learning/data/ai_market_signals.json"
trades_file="closed_trades.json"
output="app/ai/memory/signal_outcomes.json"

signals=[]
trades=[]

if os.path.exists(signals_file):
    try:
        signals=json.load(open(signals_file))
    except:
        signals=[]

if os.path.exists(trades_file):
    try:
        trades=json.load(open(trades_file))
    except:
        trades=[]


if not isinstance(signals,list):
    signals=[]

if not isinstance(trades,list):
    trades=[]


results=[]

for t in trades[-100:]:
    results.append({
        "time": t.get("time",datetime.utcnow().isoformat()),
        "symbol": t.get("symbol","UNKNOWN"),
        "profit": t.get("profit",t.get("pnl",0)),
        "status":
            "WIN" if t.get("profit",t.get("pnl",0)) > 0
            else "LOSS"
    })


data={
    "updated":datetime.utcnow().isoformat(),
    "signals_loaded":len(signals),
    "closed_trades_checked":len(trades),
    "outcomes":results[-50:]
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    data,
    open(output,"w"),
    indent=2
)

print(json.dumps({
    "signals":len(signals),
    "trades":len(trades),
    "tracked":len(data["outcomes"])
},indent=2))

print("SIGNAL TRACKER READY")

PY


echo "=== OUTPUT ===" | tee -a $LOG
cat app/ai/memory/signal_outcomes.json | head -40 | tee -a $LOG


echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "REPORT:$LOG"

