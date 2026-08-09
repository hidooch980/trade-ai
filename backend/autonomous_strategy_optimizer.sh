
#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="strategy_optimizer_$(date +%Y%m%d_%H%M%S).log"

echo "=== AUTONOMOUS STRATEGY OPTIMIZER ===" | tee -a $LOG

./venv/bin/python - <<'PY' | tee -a $LOG

import json
import os
from datetime import datetime, timezone


reinforce_file="app/ai/memory/reinforcement_weights.json"
output="app/ai/memory/optimized_strategy.json"


if os.path.exists(reinforce_file):
    try:
        data=json.load(open(reinforce_file))
    except:
        data={}
else:
    data={}


accuracy=data.get("accuracy",0)
confidence=data.get("confidence",50)
reward=data.get("total_reward",0)


if accuracy >= 60 and confidence >= 60:

    strategy="BALANCED_PLUS"
    risk_bias="NORMAL"

elif accuracy >= 50:

    strategy="CAUTIOUS_ADAPTIVE"
    risk_bias="LOW"

else:

    strategy="RECOVERY_MODE"
    risk_bias="MINIMAL"


optimized={
    "updated":datetime.now(timezone.utc).isoformat(),
    "source":"REINFORCEMENT_ENGINE",
    "accuracy":accuracy,
    "confidence":confidence,
    "reward":reward,
    "selected_strategy":strategy,
    "risk_bias":risk_bias
}


os.makedirs("app/ai/memory",exist_ok=True)

json.dump(
    optimized,
    open(output,"w"),
    indent=2
)


print(json.dumps(optimized,indent=2))
print("STRATEGY OPTIMIZED")

PY

echo "=== HEALTH ===" | tee -a $LOG

curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

