#!/bin/bash
set -e

echo "=== BACKUP ==="
cp app/decision/final_decision_engine.py app/decision/final_decision_engine.py.bak.$(date +%s)

echo "=== FIND MARKET MEMORY ==="
grep -R "class MarketMemory" -n app

echo "=== SHOW MEMORY FILE ==="
grep -R "class MarketMemory" -n app | cut -d: -f1 | xargs -I{} sh -c 'echo "--- {}"; sed -n "1,160p" {}'

echo "=== CHECK ADD USAGE ==="
grep -R "market_memory.add" -n app

echo "=== PYTHON CHECK ==="
source venv/bin/activate

python3 - <<'PY'
import os
import glob
for f in glob.glob("app/**/*.py", recursive=True):
    try:
        txt=open(f).read()
        if "class MarketMemory" in txt:
            print("FOUND:",f)
            if "def add" in txt:
                print("OK: add exists")
            else:
                print("ERROR: add missing")
    except:
        pass
PY

echo "=== SERVICE RESTART ==="
sudo systemctl restart trade-ai

sleep 5

echo "=== LOG CHECK ==="
sudo journalctl -u trade-ai -n 50 --no-pager

echo "=== DONE ==="
