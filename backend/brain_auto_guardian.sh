#!/bin/bash
cd /opt/trade-ai/backend || exit 1

LOG="brain_auto_guardian_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTO GUARDIAN START ===" | tee -a $LOG

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "=== PYTHON IMPORT SCAN ===" | tee -a $LOG
python - <<'PY' | tee -a brain_import_check.log
import importlib
mods=[
"app.ai",
"app.decision",
"app.learning",
"app.chart_ai",
"app.execution",
"app.risk",
"app.market"
]
for m in mods:
    try:
        importlib.import_module(m)
        print("OK",m)
    except Exception as e:
        print("FAIL",m,e)
PY

echo "=== BROKEN JSON SCAN ===" | tee -a $LOG
find app -name "*.json" | while read f
do
python - <<PY
import json
try:
 json.load(open("$f"))
 print("OK $f")
except Exception as e:
 print("BROKEN $f : $e")
PY
done | tee -a $LOG

echo "=== DISK ===" | tee -a $LOG
df -h | tee -a $LOG

echo "=== MEMORY ===" | tee -a $LOG
du -sh app/*memory* app/learning/data 2>/dev/null | tee -a $LOG

echo "REPORT:$LOG"
