#!/bin/bash
set -e

cd /opt/trade-ai/backend

echo "=== BACKUP ==="
cp app/learning/market_memory.py app/learning/market_memory.py.bak.$(date +%s)

echo "=== PATCH ADD METHOD ==="

python3 - <<'PY'
from pathlib import Path

p = Path("app/learning/market_memory.py")

text = p.read_text()

if "def add(" not in text:
    text = text.replace(
'''    def get_history(self):''',
'''    def add(self, data):
        return self.save(data)


    def get_history(self):'''
    )

    p.write_text(text)
    print("ADD METHOD INSERTED")
else:
    print("ADD METHOD ALREADY EXISTS")
PY


echo "=== TEST ==="

source venv/bin/activate

python3 - <<'PY'
from app.learning.market_memory import market_memory

print(market_memory.add({
    "test": "memory_fix",
    "status": "ok"
}))

print("HISTORY SIZE:", len(market_memory.get_history()))
PY


echo "=== RESTART SERVICE ==="

sudo systemctl restart trade-ai

sleep 5

echo "=== CHECK LOG ==="

sudo journalctl -u trade-ai -n 50 --no-pager

echo "=== DONE ==="
