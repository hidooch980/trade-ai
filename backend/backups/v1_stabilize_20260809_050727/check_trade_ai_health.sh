#!/bin/bash
set -e

cd /opt/trade-ai/backend
source venv/bin/activate

echo "=== SERVICE ==="
systemctl status trade-ai --no-pager | head -20

echo
echo "=== PORT 8000 ==="
ss -tulpn | grep 8000

echo
echo "=== MEMORY TEST ==="
python3 - <<'PY'
from app.learning.market_memory import market_memory

print("Memory entries:", len(market_memory.get_history()))
print("ADD TEST:", market_memory.add({"health":"ok"}))
PY

echo
echo "=== LAST LOG ==="
journalctl -u trade-ai -n 30 --no-pager

echo
echo "=== DONE ==="
