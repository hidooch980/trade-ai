
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="ai_self_evaluation_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI SELF EVALUATION ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os
from datetime import datetime

result={}

files={
"trades":"closed_trades.json",
"rewards":"app/learning/data/reward_memory.json",
"adaptive":"app/ai/memory/adaptive_strategy_weights.json"
}

for name,path in files.items():

    if os.path.exists(path):
        try:
            data=json.load(open(path))

            if isinstance(data,list):
                result[name+"_count"]=len(data)

            elif isinstance(data,dict):
                result[name]=data

        except Exception as e:
            result[name+"_error"]=str(e)


trades=result.get("trades_count",0)

wins=0
losses=0

if os.path.exists("closed_trades.json"):
    try:
        trades_data=json.load(open("closed_trades.json"))

        for t in trades_data:
            if t.get("profit",0)>0:
                wins+=1
            elif t.get("profit",0)<0:
                losses+=1

    except:
        pass


total=wins+losses

accuracy=round((wins/total)*100,2) if total else 0


evaluation={
"time":datetime.now().isoformat(),
"total_trades":trades,
"wins":wins,
"losses":losses,
"accuracy":accuracy,
"brain_state":
"IMPROVING" if accuracy>50 else "NEEDS_TUNING"
}


print(json.dumps(evaluation,indent=2))

os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
evaluation,
open("app/ai/memory/self_evaluation.json","w"),
indent=2
)

print("SELF EVALUATION SAVED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

