#!/bin/bash
cd /opt/trade-ai/backend
echo "CHECK"
python -m compileall app
echo "STATUS"
pm2 status
echo "LOG"
pm2 logs --lines 50
