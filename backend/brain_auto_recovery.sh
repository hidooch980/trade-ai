#!/bin/bash
cd /opt/trade-ai/backend || exit 1

while true
do
echo "=============================="
date
echo "=== HEALTH ==="

HEALTH=$(curl -s http://127.0.0.1:8000/health)

echo "$HEALTH"

if echo "$HEALTH" | grep -q HEALTHY
then
echo "AI STATUS: RUNNING"
else
echo "AI STATUS: DOWN"
echo "RESTARTING..."

pkill -f uvicorn 2>/dev/null
sleep 5

nohup uvicorn app.api.main:app --host 0.0.0.0 --port 8000 >/tmp/ai_recovery.log 2>&1 &

sleep 10

echo "AFTER RECOVERY:"
curl -s http://127.0.0.1:8000/health
fi

echo "=== PROCESS ==="
ps -ef | grep uvicorn | grep -v grep

echo "=== MEMORY ==="
du -sh app/memory app/neural_memory app/learning/data 2>/dev/null

sleep 60
done
