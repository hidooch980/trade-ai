#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="ai_self_evaluation_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI SELF EVALUATION ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

trade_file="closed_trades.json"
output="app/ai/memory/ai_performance.json"

if not os.path.exists(trade_file):
    print("NO TRADE DATA")
    exit()

trades=json.load(open(trade_file))

total=len(trades)
wins=0
losses=0

for t in trades:
    pnl=t.get("profit",t.get("pnl",0))

    if pnl > 0:
        wins+=1
    elif pnl < 0:
        losses+=1


accuracy=0

if total:
    accuracy=round((wins/total)*100,2)


performance={
    "time":datetime.now().isoformat(),
    "total_trades":total,
    "wins":wins,
    "losses":losses,
    "accuracy":accuracy,
    "ai_grade":
        "GOOD" if accuracy>=60
        else "NORMAL" if accuracy>=40
        else "WEAK"
}


os.makedirs(
    "app/ai/memory",
    exist_ok=True
)

json.dump(
    performance,
    open(output,"w"),
    indent=2
)

print(json.dumps(performance,indent=2))
print("SELF EVALUATION COMPLETE")

PY


echo "=== MEMORY ===" | tee -a $LOG
cat app/ai/memory/ai_performance.json | tee -a $LOG

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

