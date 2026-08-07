#!/bin/bash
cd /opt/trade-ai/backend || exit 1

LOG="trade_brain_test_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE BRAIN TEST ===" | tee -a $LOG

echo "=== MARKET DATA ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.market_data.candle.candle_builder import *
print("CANDLE ENGINE OK")
PY

echo "=== SMART MONEY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.chart_ai.smart_money.fusion.smart_money_fusion import SmartMoneyFusion
print("SMART MONEY OK")
PY

echo "=== DECISION ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.decision.final_decision_engine import FinalDecisionEngine
print("DECISION OK")
PY

echo "=== RISK ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.risk.risk_manager import RiskManager
print("RISK OK")
PY

echo "=== EXECUTION ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.trade_executor import TradeExecutor
print("EXECUTOR OK")
PY

echo "=== CLOSE SYSTEM ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.execution.close_manager import CloseManager
print("CLOSE MANAGER OK")
PY

echo "REPORT:$LOG"
