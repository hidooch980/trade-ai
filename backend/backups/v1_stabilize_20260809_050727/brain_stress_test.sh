#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_stress_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN STRESS TEST ===" | tee -a $LOG

echo "=== SYSTEM BEFORE ===" | tee -a $LOG
free -h | tee -a $LOG
top -bn1 | head -20 | tee -a $LOG

echo "=== MULTI SIGNAL TEST ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
from app.decision.final_decision_engine import FinalDecisionEngine

engine = FinalDecisionEngine()

symbols=[
"BTCUSD",
"ETHUSD",
"EURUSD",
"GBPUSD",
"XAUUSD",
"USDJPY",
]

for s in symbols:
    signal={
        "symbol":s,
        "direction":"BUY",
        "confidence":90,
        "score":85
    }

    try:
        result=engine.decide(
            indicator_signal=signal,
            ai_signal=signal,
            risk={"allowed":True},
            smart_money={"score":85}
        )
        print(s, "OK", result.get("decision"))
    except Exception as e:
        print(s, "ERROR", e)

PY

echo "=== SYSTEM AFTER ===" | tee -a $LOG
free -h | tee -a $LOG
top -bn1 | head -20 | tee -a $LOG

echo "=== API ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"
