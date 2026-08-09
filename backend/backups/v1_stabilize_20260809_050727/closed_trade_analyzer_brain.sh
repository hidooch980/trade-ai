#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="closed_trade_analyzer_$(date +%Y%m%d_%H%M%S).log"

echo "=== CLOSED TRADE ANALYZER BRAIN ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


position_file="positions.json"
reward_file="app/learning/data/reward_memory.json"
output="app/ai/memory/closed_trade_analysis.json"


def load(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except:
            return default
    return default


positions=load(position_file,[])
rewards=load(reward_file,[])


closed=[]

for p in positions:

    if p.get("status")=="CLOSED":

        pnl=p.get("profit",p.get("pnl",0))

        if pnl < 0:
            result="LOSS"
            lesson="REDUCE_ENTRY_CONFIDENCE"
        elif pnl > 0:
            result="WIN"
            lesson="KEEP_STRATEGY"
        else:
            result="BREAKEVEN"
            lesson="NEUTRAL"


        closed.append({
            "ticket":p.get("ticket"),
            "symbol":p.get("symbol"),
            "pnl":pnl,
            "result":result,
            "lesson":lesson
        })


losses=sum(1 for x in closed if x["result"]=="LOSS")
wins=sum(1 for x in closed if x["result"]=="WIN")


analysis={
    "time":datetime.now(timezone.utc).isoformat(),
    "engine":"CLOSED_TRADE_ANALYZER",
    "closed_trades":len(closed),
    "wins":wins,
    "losses":losses,
    "analysis":closed,
    "brain_update":
        "DEFENSIVE" if losses>wins else "NORMAL"
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    analysis,
    open(output,"w"),
    indent=2
)


print(json.dumps(analysis,indent=2))
print("CLOSED TRADE ANALYSIS COMPLETE")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

