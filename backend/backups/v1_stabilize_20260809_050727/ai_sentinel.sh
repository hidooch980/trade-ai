#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="sentinel.log"

while true
do
echo "===== $(date) =====" >> $LOG

HEALTH=$(curl -s http://127.0.0.1:8000/health)

if echo "$HEALTH" | grep -q HEALTHY
then
echo "API OK" >> $LOG
else
echo "API DOWN - CHECK REQUIRED" >> $LOG
fi

python -m compileall app >/tmp/compile_check.log 2>&1

if [ $? -eq 0 ]
then
echo "PYTHON OK" >> $LOG
else
echo "PYTHON ERROR" >> $LOG
cat /tmp/compile_check.log >> $LOG
fi

ps aux | grep uvicorn | grep -v grep >> $LOG

sleep 300

done
