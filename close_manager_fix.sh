#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/trade-ai/backend
source ../.venv/bin/activate

python3 - <<'PY'
p="app/execution/close_manager.py"
s=open(p).read()

if "position_store" not in s:
    s=s.replace(
        "class CloseManager:",
        "from app.execution.position_store import position_store\n\nclass CloseManager:"
    )

open(p,"w").write(s)
PY

echo "=== COMPILE ==="
python3 -m py_compile app/execution/close_manager.py

echo "=== RESTART API ==="
pkill -9 -f uvicorn || true
sleep 2

nohup uvicorn app.api.main:app --host 0.0.0.0 --port 8000 >/tmp/trade-ai.log 2>&1 &

sleep 5

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
