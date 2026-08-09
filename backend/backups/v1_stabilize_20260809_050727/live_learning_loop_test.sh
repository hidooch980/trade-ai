#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="live_learning_loop_$(date +%Y%m%d_%H%M%S).log"

echo "=== LIVE LEARNING LOOP TEST ===" | tee -a $LOG

echo "=== MARKET FEED ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
try:
    from app.market.stream.market_stream_worker import *
    print("MARKET STREAM OK")
except Exception as e:
    print("MARKET STREAM ERROR:", e)
PY

echo "=== PRICE PROVIDER ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
try:
    from app.market.stream.price_provider import *
    print("PRICE PROVIDER OK")
except Exception as e:
    print("PRICE PROVIDER ERROR:", e)
PY

echo "=== MARKET MEMORY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
from app.learning.market_memory import *
print("MARKET MEMORY OK")
PY

echo "=== REWARD ENGINE ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
try:
    from app.learning.reward_engine import *
    print("REWARD ENGINE OK")
except Exception as e:
    print("REWARD ERROR:", e)
PY

echo "=== ADAPTIVE MEMORY ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
try:
    from app.ai.memory.adaptive_strategy_memory import *
    print("ADAPTIVE MEMORY OK")
except Exception as e:
    print("ADAPTIVE MEMORY ERROR:", e)
PY

echo "=== REPORT ==="
echo "$LOG"
