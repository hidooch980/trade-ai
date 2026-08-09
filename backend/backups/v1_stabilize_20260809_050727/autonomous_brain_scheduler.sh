#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="brain_scheduler_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTONOMOUS BRAIN SCHEDULER ===" | tee -a $LOG

run_task(){

NAME=$1
CMD=$2

echo "=== RUN $NAME ===" | tee -a $LOG

eval "$CMD" >> $LOG 2>&1

if [ $? -eq 0 ]
then
 echo "$NAME OK" | tee -a $LOG
else
 echo "$NAME FAILED" | tee -a $LOG
fi

}


run_task "HEALTH" \
"curl -s http://127.0.0.1:8000/health"


run_task "MEMORY_GUARDIAN" \
"./memory_guardian.sh"


run_task "PERFORMANCE" \
"./brain_performance_monitor.sh"


run_task "METRICS" \
"./brain_metrics_collector.sh"


run_task "ADAPTIVE" \
"./adaptive_strategy_brain.sh"


run_task "RECOVERY" \
"curl -s http://127.0.0.1:8000/health"


echo "=== SCHEDULER COMPLETE ===" | tee -a $LOG

echo "REPORT:$LOG"

