#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_release_check_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN RELEASE CHECK ===" | tee -a $LOG

echo "=== GIT STATUS ===" | tee -a $LOG
git status | tee -a $LOG

echo "=== PYTHON COMPILE CHECK ===" | tee -a $LOG
python -m compileall app -q
if [ $? -eq 0 ]; then
    echo "PYTHON COMPILE OK" | tee -a $LOG
else
    echo "PYTHON COMPILE FAILED" | tee -a $LOG
fi

echo "=== JSON MEMORY CHECK ===" | tee -a $LOG
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

echo "=== LARGE FILE CHECK ===" | tee -a $LOG
find app -type f -size +5M -ls | tee -a $LOG

echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"
