#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/trade-ai
source .venv/bin/activate
cd backend

echo "=== STOP OLD API ==="
pkill -9 -f uvicorn || true
sleep 2

echo "=== START API ==="
nohup uvicorn app.api.main:app --host 0.0.0.0 --port 8000 >/tmp/trade-ai.log 2>&1 &

sleep 5

echo "=== HEALTH ==="
curl -s http://127.0.0.1:8000/health

echo
echo "=== MARKET STATUS ==="
curl -s http://127.0.0.1:8000/market/status

echo
echo "=== DASHBOARD ==="
curl -s http://127.0.0.1:8000/dashboard/status

echo
echo "=== SIGNAL ==="
curl -s http://127.0.0.1:8000/signal

echo
echo "=== POSITIONS ==="
curl -s http://127.0.0.1:8000/api/trading/positions

echo
echo "=== HISTORY ==="
curl -s http://127.0.0.1:8000/api/trading/history

echo
echo "=== ROUTES ==="
curl -s http://127.0.0.1:8000/openapi.json | grep -o '"/[^"]*"'

echo
echo "=== DONE ==="
