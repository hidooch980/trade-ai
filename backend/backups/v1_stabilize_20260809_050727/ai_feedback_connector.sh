#!/bin/bash

cd /opt/trade-ai/backend || exit 1

LOG="ai_feedback_connector_$(date +%Y%m%d_%H%M%S).log"

echo "=== AI DECISION FEEDBACK CONNECTOR ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
import json
import os

memory="app/ai/memory/adaptive_strategy_weights.json"

if not os.path.exists(memory):
    print("ADAPTIVE MEMORY NOT FOUND")
    exit()

data=json.load(open(memory))

confidence=data.get("adaptive_confidence",50)
status=data.get("strategy_status","NEUTRAL")

multiplier=1.0

if status=="POSITIVE":
    multiplier=1.05
elif status=="NEGATIVE":
    multiplier=0.90


connector={
    "adaptive_status":status,
    "base_confidence":confidence,
    "decision_multiplier":multiplier,
    "enabled":True
}

output="app/ai/memory/decision_feedback.json"

json.dump(
    connector,
    open(output,"w"),
    indent=2
)

print(json.dumps(connector,indent=2))
print("FEEDBACK CONNECTOR ENABLED")

PY


echo "=== TEST DECISION ENGINE ===" | tee -a $LOG

python - <<'PY' | tee -a $LOG
from app.decision.final_decision_engine import FinalDecisionEngine

engine=FinalDecisionEngine()

result=engine.decide(
    indicator_signal={
        "direction":"BUY",
        "score":80
    },
    ai_signal={
        "direction":"BUY",
        "confidence":80
    },
    risk={
        "allowed":True
    },
    smart_money={
        "score":80
    }
)

print(result)

PY


echo "=== HEALTH ===" | tee -a $LOG
curl -s http://127.0.0.1:8000/health | tee -a $LOG

echo "REPORT:$LOG"

