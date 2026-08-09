#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="guardian_daemon_$(date +%Y%m%d_%H%M%S).log"

echo "=== GUARDIAN DAEMON STARTED ===" | tee -a $LOG


while true
do

echo "$(date) RUN CYCLE" | tee -a $LOG


./live_position_supervisor.sh >> $LOG 2>&1

./supervisor_guardian_sync.sh >> $LOG 2>&1

./guardian_action_executor.sh >> $LOG 2>&1


echo "$(date) CYCLE COMPLETE" | tee -a $LOG


sleep 30


done

