#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="trade_learning_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE LEARNING LOOP ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

source="closed_trades.json"
memory="app/learning/data/reward_memory.json"

if not os.path.exists(source):
    print("NO CLOSED TRADES")
    exit()

trades=json.load(open(source))

wins=0
losses=0
reward=0

for t in trades:
    profit=t.get("profit", t.get("pnl",0))

    if profit > 0:
        wins+=1
        reward+=1
    elif profit < 0:
        losses+=1
        reward-=1

print("TRADES:",len(trades))
print("WINS:",wins)
print("LOSSES:",losses)
print("TOTAL REWARD:",reward)


data=[]

if os.path.exists(memory):
    try:
        data=json.load(open(memory))
    except:
        data=[]

if not isinstance(data,list):
    data=[]

data.append({
    "time":datetime.utcnow().isoformat(),
    "trades":len(trades),
    "wins":wins,
    "losses":losses,
    "reward":reward
})

json.dump(data,open(memory,"w"),indent=2)

print("REWARD MEMORY UPDATED")
print("MEMORY SIZE:",len(data))

PY


echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

