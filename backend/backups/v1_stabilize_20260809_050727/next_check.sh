#!/bin/bash
cd /opt/trade-ai/backend || exit 1
echo "=== API HEALTH ==="
curl -s http://127.0.0.1:8000/health || true
echo
echo "=== IMPORT TEST ==="
python - <<'PY'
import app
print("APP IMPORT OK")
PY
echo "=== PROCESS ==="
ps -fp 1961
echo "=== ERRORS ==="
find . -name "*.log" -type f | tail -10
