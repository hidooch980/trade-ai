#!/bin/bash
cd /opt/trade-ai/backend || exit 1
echo "=== GIT ==="
git status
echo "=== PYTHON ==="
python --version
echo "=== FILES ==="
find app -maxdepth 2 -type f | head -50
echo "=== PM2 ==="
pm2 status
echo "=== PORTS ==="
ss -tulpn | grep -E '3000|8000|8080|5173'
echo "=== LOGS ==="
pm2 logs --lines 100 --nostream
