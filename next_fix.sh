#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/trade-ai/backend
source ../.venv/bin/activate

echo "=== FIX DUPLICATE POSITION ==="

python3 - <<'PY'
p="app/execution/trade_executor.py"
s=open(p).read()

s=s.replace(
'from app.execution.position_store import position_store\nfrom app.execution.position_store import position_store',
'from app.execution.position_store import position_store'
)

old='''        position_store.add({"ticket": mt5_result.get("ticket","SIM-1"),"symbol": symbol,"side": signal["decision"],"volume": risk["volume"],"entry_price": order["price"],"current_price": order["price"],"pnl":0.0,"stop_loss":risk.get("stop_loss"),"take_profit":risk.get("take_profit")})\n\n        position_store.add({"ticket": mt5_result.get("ticket","SIM-1"),"symbol": symbol,"side": signal["decision"],"volume": risk["volume"],"entry_price": order["price"],"current_price": order["price"],"pnl":0.0,"stop_loss":risk.get("stop_loss"),"take_profit":risk.get("take_profit")})'''

new='''        position_store.add({"ticket": mt5_result.get("ticket","SIM-1"),"symbol": symbol,"side": signal["decision"],"volume": risk["volume"],"entry_price": order["price"],"current_price": order["price"],"pnl":0.0,"stop_loss":risk.get("stop_loss"),"take_profit":risk.get("take_profit")})'''

s=s.replace(old,new)

open(p,"w").write(s)
PY

echo "=== COMPILE ==="
python3 -m py_compile app/execution/trade_executor.py

echo "=== RESTART ==="
pkill -9 -f uvicorn || true
sleep 2

cd ~/trade-ai
source .venv/bin/activate
cd backend

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
echo "=== OPENAPI ==="
curl -s http://127.0.0.1:8000/openapi.json | grep -o '"/[^"]*"'

echo
echo "=== DONE ==="
