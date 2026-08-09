
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="trade_result_analyzer_$(date +%Y%m%d_%H%M%S).log"

echo "=== TRADE RESULT ANALYZER ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

source="closed_trades.json"
output="app/ai/memory/trade_analysis.json"

wins=0
losses=0
neutral=0
total=0
profit_sum=0

if os.path.exists(source):

    data=json.load(open(source))

    print("TOTAL RECORDS:",len(data))

    for t in data:

        total+=1

        profit=0

        for key in [
            "profit",
            "pnl",
            "net_profit",
            "close_profit",
            "result"
        ]:
            if key in t:
                try:
                    profit=float(t[key])
                    break
                except:
                    pass


        profit_sum+=profit

        if profit>0:
            wins+=1
        elif profit<0:
            losses+=1
        else:
            neutral+=1


accuracy=round((wins/(wins+losses))*100,2) if (wins+losses)>0 else 0


report={
"time":datetime.now().isoformat(),
"total":total,
"wins":wins,
"losses":losses,
"neutral":neutral,
"profit_sum":profit_sum,
"accuracy":accuracy,
"status":
"GOOD" if accuracy>50 else "NEEDS_OPTIMIZATION"
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
report,
open(output,"w"),
indent=2
)

print(json.dumps(report,indent=2))
print("ANALYSIS SAVED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

