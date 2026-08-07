#!/bin/bash

cd /opt/trade-ai/backend || exit 1

REPORT="ai_repair_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE AI AUTO REPAIR ===" | tee $REPORT

echo "=== BACKUP STATUS ===" | tee -a $REPORT
git status --short | tee -a $REPORT

echo "=== CLEAN CACHE ===" | tee -a $REPORT
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

echo "CACHE OK" | tee -a $REPORT


echo "=== PYTHON COMPILE TEST ===" | tee -a $REPORT
python -m compileall app 2>&1 | tee -a $REPORT


echo "=== IMPORT SCAN ===" | tee -a $REPORT
python - <<'PY' 2>&1 | tee -a import_scan.log
import pkgutil
import app

failed=[]

for m in pkgutil.walk_packages(app.__path__, app.__name__+"."):
    try:
        __import__(m.name)
    except Exception as e:
        failed.append((m.name,str(e)))

print("FAILED IMPORTS:")
for x in failed:
    print(x)
PY


echo "=== DEPENDENCY CHECK ===" | tee -a $REPORT
if [ -f requirements.txt ]; then
    pip install -r requirements.txt 2>&1 | tee -a $REPORT
fi


echo "=== FINAL HEALTH ===" | tee -a $REPORT
curl -s http://127.0.0.1:8000/health | tee -a $REPORT


echo "=== REPAIR FINISHED ===" | tee -a $REPORT
echo "REPORT: $REPORT"

