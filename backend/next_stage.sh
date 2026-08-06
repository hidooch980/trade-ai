#!/data/data/com.termux/files/usr/bin/bash
set -e
source ../.venv/bin/activate
python3 -m py_compile app/execution/*.py app/api/routes/*.py
echo "=== CORE CHECK OK ==="
curl -s http://127.0.0.1:8000/health
echo
curl -s http://127.0.0.1:8000/api/trading/positions
echo
curl -s http://127.0.0.1:8000/api/trading/history
echo
echo "=== NEXT STAGE READY ==="
