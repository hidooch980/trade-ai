#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="recovery_manager_$(date +%Y%m%d_%H%M%S).log"

echo "=== RECOVERY MANAGER ===" | tee -a $LOG

echo "=== BACKUP CHECK ===" | tee -a $LOG

ls -lh brain_backup_*.tar.gz 2>/dev/null | tee -a $LOG


echo "=== MODULE HEALTH ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import os, importlib

errors=[]

for root,dirs,files in os.walk("app"):
    for f in files:
        if f.endswith(".py") and not f.startswith("."):
            module=os.path.join(root,f).replace("/",".")[:-3]

            try:
                importlib.import_module(module)
            except Exception as e:
                errors.append({
                    "module":module,
                    "error":str(e)
                })

if errors:
    print("ERROR MODULES:")
    for e in errors:
        print(e)
else:
    print("ALL MODULES HEALTHY")

PY


echo "=== API HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "=== RECOVERY READY ===" | tee -a $LOG

echo "REPORT:$LOG"

