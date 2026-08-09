#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="autonomous_loop_$(date +%Y%m%d_%H%M%S).log"

echo "=== FINAL AUTONOMOUS LOOP START ===" | tee -a $LOG

while true
do

echo "==============================" | tee -a $LOG
date | tee -a $LOG

echo "=== HEALTH CHECK ===" | tee -a $LOG

HEALTH=$(curl -s http://127.0.0.1:8000/health)

echo "$HEALTH" | tee -a $LOG


if echo "$HEALTH" | grep -q HEALTHY
then

echo "BRAIN STATUS: ONLINE" | tee -a $LOG

else

echo "BRAIN STATUS: OFFLINE" | tee -a $LOG
echo "STARTING RECOVERY" | tee -a $LOG


pkill -f uvicorn 2>/dev/null

sleep 5

nohup ./run.sh >> autonomous_recovery.log 2>&1 &

sleep 15

echo "RECOVERY RESULT:" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

fi


echo "=== COMMAND CENTER ===" | tee -a $LOG

./brain_command_center.sh >> $LOG 2>&1


echo "=== MEMORY SIZE ===" | tee -a $LOG

du -sh app/memory app/neural_memory app/learning/data 2>/dev/null | tee -a $LOG


echo "SLEEP 60s" | tee -a $LOG

sleep 60

done

