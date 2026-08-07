#!/bin/bash

cd /opt/trade-ai/backend || exit 1

REPORT="ai_doctor_report_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE AI AUTO DOCTOR ===" | tee $REPORT
echo "TIME: $(date)" | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== API HEALTH ===" | tee -a $REPORT
curl -s http://127.0.0.1:8000/health | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== PYTHON VERSION ===" | tee -a $REPORT
python --version | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== SYNTAX CHECK ===" | tee -a $REPORT
python -m compileall app 2>&1 | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== IMPORT TEST ===" | tee -a $REPORT
python - <<'PY' 2>&1 | tee -a ai_import_error.log
import app
print("IMPORT OK")
PY

echo "" | tee -a $REPORT
echo "=== SEARCH ERRORS ===" | tee -a $REPORT
grep -R "ERROR\|Exception\|Traceback\|failed" . \
--include="*.log" \
--include="*.py" \
2>/dev/null | tail -100 | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== RUNNING PROCESS ===" | tee -a $REPORT
ps aux | grep uvicorn | grep -v grep | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== PORT 8000 ===" | tee -a $REPORT
ss -tulpn | grep 8000 | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== CLEAN PYTHON CACHE ===" | tee -a $REPORT
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

echo "CACHE CLEANED" | tee -a $REPORT

echo "" | tee -a $REPORT
echo "=== DONE ===" | tee -a $REPORT
echo "REPORT: $REPORT"

