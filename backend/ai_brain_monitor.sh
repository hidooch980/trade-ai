#!/bin/bash

cd /opt/trade-ai/backend || exit 1

REPORT="brain_status_$(date +%Y%m%d_%H%M%S).log"

echo "===== TRADE AI BRAIN MONITOR =====" | tee $REPORT
echo "TIME: $(date)" | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== MODULE COUNT ===" | tee -a $REPORT
find app -name "*.py" | wc -l | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== AI MODULES ===" | tee -a $REPORT
find app/ai app/decision app/learning app/chart_ai \
-name "*.py" 2>/dev/null | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== IMPORT HEALTH ===" | tee -a $REPORT
python - <<'PY' 2>&1 | tee -a $REPORT
modules=[
"app.ai",
"app.decision",
"app.learning",
"app.chart_ai",
"app.execution",
"app.risk",
"app.market"
]

for m in modules:
    try:
        __import__(m)
        print(m,"OK")
    except Exception as e:
        print(m,"ERROR",e)
PY

echo "" | tee -a $REPORT
echo "=== API ===" | tee -a $REPORT
curl -s http://127.0.0.1:8000/health | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== MEMORY FILES ===" | tee -a $REPORT
find app -iname "*memory*" -o -iname "*brain*" | tee -a $REPORT

echo "" | tee -a $REPORT
echo "DONE: $REPORT"

