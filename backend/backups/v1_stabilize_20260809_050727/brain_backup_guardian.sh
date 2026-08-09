#!/bin/bash

cd /opt/trade-ai/backend || exit 1

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP="brain_backup_$DATE"

mkdir -p "$BACKUP"

echo "=== AI BRAIN BACKUP ==="

cp -r app/ai "$BACKUP/" 2>/dev/null
cp -r app/decision "$BACKUP/" 2>/dev/null
cp -r app/learning/data "$BACKUP/" 2>/dev/null
cp -r app/memory "$BACKUP/" 2>/dev/null
cp -r app/neural_memory "$BACKUP/" 2>/dev/null

tar -czf "$BACKUP.tar.gz" "$BACKUP"

rm -rf "$BACKUP"

echo "BACKUP CREATED:"
echo "$BACKUP.tar.gz"

ls -lh "$BACKUP.tar.gz"
