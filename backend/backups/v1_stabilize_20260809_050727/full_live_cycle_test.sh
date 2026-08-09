#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="full_live_cycle_$(date +%Y%m%d_%H%M%S).log"

echo "=== FULL LIVE TRADE CYCLE ===" | tee -a $LOG

echo "=== MARKET LOOP ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.market.loop.live_market_runner import live_market_runner
print("LIVE MARKET RUNNER OK")
print(live_market_runner)
PY

echo "=== SIGNAL GENERATION ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.trading.pipeline.signal_pipeline import SignalPipeline
print("SIGNAL PIPELINE READY")
PY

echo "=== DECISION FLOW ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.decision.final_decision_engine import FinalDecisionEngine

engine = FinalDecisionEngine()

test_signal={
"symbol":"BTCUSD",
"direction":"BUY",
"confidence":90,
"score":90
}

result=engine.decide(
indicator_signal=test_signal,
ai_signal=test_signal,
risk={"allowed":True},
smart_money={"score":90}
)

print(result)
PY

echo "=== POSITION MANAGEMENT ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.position_manager import PositionManager
print("POSITION MANAGER OK")
print(PositionManager)
PY

echo "=== TRADE HISTORY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.trade_history import TradeHistory
print("TRADE HISTORY OK")
print(TradeHistory)
PY

echo "=== MEMORY LEARNING ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.learning.market_memory import *
print("MARKET MEMORY OK")
PY

echo "REPORT:$LOG"
