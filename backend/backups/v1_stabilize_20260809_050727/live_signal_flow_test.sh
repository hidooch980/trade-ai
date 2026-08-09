#!/bin/bash
cd /opt/trade-ai/backend || exit 1

LOG="live_signal_flow_$(date +%Y%m%d_%H%M%S).log"

echo "=== LIVE SIGNAL FLOW TEST ===" | tee -a $LOG

echo "=== SIGNAL PIPELINE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.trading.pipeline.signal_pipeline import SignalPipeline
print("PIPELINE LOAD OK")
print(SignalPipeline)
PY

echo "=== AI DECISION TEST ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.decision.final_decision_engine import FinalDecisionEngine

engine = FinalDecisionEngine()

signal = {
    "symbol":"BTCUSD",
    "direction":"BUY",
    "confidence":85,
    "score":80
}

try:
    result = engine.decide(
        indicator_signal=signal,
        ai_signal=signal,
        risk={"allowed":True},
        smart_money={"score":80}
    )
    print("DECISION RESULT:", result)
except Exception as e:
    print("DECISION ERROR:", e)
PY

echo "=== POSITION STORE TEST ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.position_store import position_store

print("STORE LOAD OK")
print(position_store)
PY

echo "=== REPORT ==="
echo "$LOG"
