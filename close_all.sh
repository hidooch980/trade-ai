#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/trade-ai
source .venv/bin/activate
cd backend

echo "=== CLOSE ALL POSITIONS ==="

python3 - <<'PY'
from app.execution.position_store import position_store

count=len(position_store.get_all())
position_store.positions=[]

print({"closed_positions":count,"status":"ALL_CLOSED"})
PY

echo "=== VERIFY ==="
curl -s http://127.0.0.1:8000/api/trading/positions

echo
echo "=== DONE ==="
