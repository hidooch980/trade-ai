#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_performance_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN PERFORMANCE MONITOR ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import time

tests = {}

def measure(name, func):
    start=time.time()
    try:
        func()
        tests[name]=round((time.time()-start)*1000,2)
        print(name, "OK", tests[name], "ms")
    except Exception as e:
        print(name, "FAIL", e)


measure(
"AI_IMPORT",
lambda: __import__("app.ai")
)

measure(
"DECISION_ENGINE",
lambda: __import__("app.decision.final_decision_engine")
)

measure(
"SIGNAL_PIPELINE",
lambda: __import__("app.trading.pipeline.signal_pipeline")
)

measure(
"EXECUTION_ENGINE",
lambda: __import__("app.execution.trade_executor")
)

measure(
"RISK_ENGINE",
lambda: __import__("app.risk.risk_manager")
)


print("===================")
print("PERFORMANCE REPORT")

for k,v in tests.items():
    print(k,":",v,"ms")

PY


echo "=== API LATENCY ===" | tee -a $LOG

START=$(date +%s%3N)
curl -s http://127.0.0.1:8000/health >/dev/null
END=$(date +%s%3N)

echo "HEALTH RESPONSE TIME: $((END-START)) ms" | tee -a $LOG


echo "REPORT:$LOG"

