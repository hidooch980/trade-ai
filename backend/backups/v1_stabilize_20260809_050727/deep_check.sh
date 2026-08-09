#!/bin/bash
cd /opt/trade-ai/backend || exit 1
echo "=== UVICORN COMMAND ==="
ps -fp 1961
echo
echo "=== OPEN PORT 8000 ==="
ss -lntp | grep 8000
echo
echo "=== ROUTES ==="
python - <<'PY'
from app.api.main import app
for r in app.routes:
    print(getattr(r,"path",r))
PY
echo
echo "=== EXECUTION FILES ==="
ls -la app/execution
echo
echo "=== POSITION STORE TEST ==="
python - <<'PY'
from app.execution.position_store import position_store
print(position_store)
try:
    print(position_store.get_all())
except Exception as e:
    print("STORE ERROR:",e)
PY
echo
echo "=== MEMORY TEST ==="
python - <<'PY'
from app.learning.market_memory import *
print("MARKET MEMORY IMPORT OK")
PY
