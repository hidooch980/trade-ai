#!/bin/bash

echo "=== TRADE-AI SYSTEM CHECK ==="

echo
echo "=== SERVICE STATUS ==="
systemctl status trade-ai --no-pager | head -30

echo
echo "=== UVICORN PROCESS ==="
ps aux | grep uvicorn | grep -v grep

echo
echo "=== PORT 8000 ==="
ss -tulpn | grep 8000

echo
echo "=== API HEALTH ==="
curl -s http://127.0.0.1/api/trading/positions

echo
echo
echo "=== POSITIONS FILE ==="
cat /opt/trade-ai/backend/positions.json 2>/dev/null || echo "NO POSITIONS FILE"

echo
echo "=== POSITION STORE TEST ==="
python3 - <<'PY'
from app.execution.position_store import position_store,STORE_FILE
print("STORE FILE:",STORE_FILE)
print("STORE DATA:",position_store.get_all())
PY

echo
echo "=== TICKET TEST ==="
python3 - <<'PY'
from app.execution.ticket_manager import ticket_manager,COUNTER_FILE
print("COUNTER FILE:",COUNTER_FILE)
print("LAST:",ticket_manager.counter)
PY

echo
echo "=== ROUTES ==="
grep -Rni 'router.post\|router.get' app/api/routes --include="*.py"

echo
echo "=== EXECUTE PIPELINE ==="
grep -Rni "execute(" app --include="*.py" | head -30

echo
echo "=== MARKET TICK TEST ==="
curl -s -X POST http://127.0.0.1/api/trading/tick/2500

echo
echo
echo "=== LAST LOGS ==="
journalctl -u trade-ai -n 50 --no-pager

echo
echo "=== DONE ==="
