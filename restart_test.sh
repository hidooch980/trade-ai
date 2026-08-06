#!/data/data/com.termux/files/usr/bin/bash
cd ~/trade-ai
source .venv/bin/activate
cd backend

echo "=== STOP UVICORN ==="
pkill -f uvicorn || true

echo "=== START API ==="
nohup uvicorn app.api.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

sleep 3

echo "=== HEALTH ==="
curl -s http://127.0.0.1:8000/health

echo
echo "=== POSITIONS ==="
curl -s http://127.0.0.1:8000/api/trading/positions

echo
echo "=== HISTORY ==="
curl -s http://127.0.0.1:8000/api/trading/history

echo
echo "=== DONE ==="
