#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_snapshot_$(date +%Y%m%d_%H%M%S).log"

echo "=== BRAIN SNAPSHOT RELEASE ===" | tee -a $LOG

echo "=== CURRENT BRANCH ===" | tee -a $LOG
git branch --show-current | tee -a $LOG

echo "=== ADD CHANGES ===" | tee -a $LOG
git add app data *.sh 2>/dev/null

echo "=== COMMIT ===" | tee -a $LOG
git commit -m "release: Brain AI stable checkpoint v1.0" | tee -a $LOG

echo "=== TAG ===" | tee -a $LOG
git tag -a brain-v1.0 -m "Trade AI Brain stable version 1.0" 2>/dev/null || true

echo "=== LAST COMMITS ===" | tee -a $LOG
git --no-pager log --oneline -5 | tee -a $LOG

echo "=== STATUS ===" | tee -a $LOG
git status | tee -a $LOG

echo "REPORT:$LOG"
