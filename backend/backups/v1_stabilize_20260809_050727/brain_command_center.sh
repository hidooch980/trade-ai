
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_center_$(date +%Y%m%d_%H%M%S).log"

echo "================================" | tee -a $LOG
echo "       AI BRAIN COMMAND CENTER" | tee -a $LOG
echo "================================" | tee -a $LOG


echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG


echo "" | tee -a $LOG
echo "=== PROCESS ===" | tee -a $LOG
ps -ef | grep uvicorn | grep -v grep | tee -a $LOG


echo "" | tee -a $LOG
echo "=== MEMORY ===" | tee -a $LOG
du -sh app/memory app/neural_memory app/learning/data 2>/dev/null | tee -a $LOG


echo "" | tee -a $LOG
echo "=== PERFORMANCE ===" | tee -a $LOG
if [ -f app/ai/memory/ai_performance.json ]
then
cat app/ai/memory/ai_performance.json | tee -a $LOG
else
echo "NO PERFORMANCE FILE" | tee -a $LOG
fi


echo "" | tee -a $LOG
echo "=== ADAPTIVE ===" | tee -a $LOG
if [ -f app/ai/memory/adaptive_strategy_weights.json ]
then
cat app/ai/memory/adaptive_strategy_weights.json | tee -a $LOG
fi


echo "" | tee -a $LOG
echo "=== RECENT REPORTS ===" | tee -a $LOG
ls -lt *.log | head -10 | tee -a $LOG


echo "" | tee -a $LOG
echo "=== COMMAND CENTER READY ===" | tee -a $LOG

echo "REPORT:$LOG"

