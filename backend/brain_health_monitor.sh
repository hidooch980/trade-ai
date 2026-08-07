#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_health_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI BRAIN HEALTH MONITOR ===" | tee -a $LOG

while true
do

echo "-----------------------------" | tee -a $LOG
date | tee -a $LOG

echo "=== API ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "=== PROCESS ===" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG

echo "=== MEMORY ===" | tee -a $LOG
du -sh app/memory app/neural_memory app/learning/data 2>/dev/null | tee -a $LOG

echo "=== DISK ===" | tee -a $LOG
df -h / | tail -1 | tee -a $LOG

echo "=== PYTHON ===" | tee -a $LOG
python - <<'PY' | tee -a $LOG
import gc
print("GC OBJECTS:",len(gc.get_objects()))
print("BRAIN STATUS: RUNNING")
PY

sleep 60

done
