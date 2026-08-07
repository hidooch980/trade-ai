#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="memory_guardian_$(date +%Y%m%d_%H%M%S).log"

echo "=== MEMORY GUARDIAN ===" | tee $LOG

for f in $(find app -name "*.json" 2>/dev/null)
do
python - <<PY 2>/dev/null
import json
try:
    json.load(open("$f"))
    print("OK $f")
except Exception as e:
    print("BROKEN $f : $e")
PY
done | tee -a $LOG

echo "=== MEMORY SIZE ===" | tee -a $LOG
du -sh app/*memory* app/learning/data 2>/dev/null | tee -a $LOG

echo "REPORT $LOG"
