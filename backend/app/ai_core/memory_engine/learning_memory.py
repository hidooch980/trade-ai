import json
from pathlib import Path

MEMORY_FILE=Path("data/ai_learning_memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"trades":[],"performance":{"wins":0,"losses":0}}

def save_trade(trade):
    memory=load_memory()
    memory["trades"].append(trade)

    if trade.get("pnl",0)>0:
        memory["performance"]["wins"]+=1
    else:
        memory["performance"]["losses"]+=1

    MEMORY_FILE.parent.mkdir(exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory,indent=2))
    return memory

def learning_score():
    memory=load_memory()
    total=memory["performance"]["wins"]+memory["performance"]["losses"]
    if total==0:
        return 50
    return round((memory["performance"]["wins"]/total)*100)

