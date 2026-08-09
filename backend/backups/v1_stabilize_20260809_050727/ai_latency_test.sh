#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="ai_latency_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI LATENCY TEST ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import time
from app.decision.final_decision_engine import FinalDecisionEngine

engine=FinalDecisionEngine()

signal={
"symbol":"BTCUSD",
"direction":"BUY",
"confidence":90,
"score":90
}

times=[]

for i in range(100):

    start=time.time()

    try:
        engine.decide(
            indicator_signal=signal,
            ai_signal=signal,
            risk={"allowed":True},
            smart_money={"score":90}
        )

        elapsed=(time.time()-start)*1000
        times.append(elapsed)

    except Exception as e:
        print("ERROR:",e)

if times:
    print("COUNT:",len(times))
    print("MIN_MS:",min(times))
    print("MAX_MS:",max(times))
    print("AVG_MS:",sum(times)/len(times))

PY

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"
