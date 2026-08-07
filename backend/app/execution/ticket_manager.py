import json
from pathlib import Path

COUNTER_FILE=Path("/opt/trade-ai/backend/ticket_counter.json")

class TicketManager:
    def __init__(self):
        self.counter=0
        self.load()

    def load(self):
        if COUNTER_FILE.exists():
            try:
                self.counter=json.loads(COUNTER_FILE.read_text()).get("last_ticket",0)
            except:
                self.counter=0

    def save(self):
        COUNTER_FILE.write_text(json.dumps({"last_ticket":self.counter}))

    def new(self):
        self.counter+=1
        self.save()
        return f"SIM-{self.counter}"


ticket_manager=TicketManager()
