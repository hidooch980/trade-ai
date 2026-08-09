from datetime import datetime

class TradeJournal:
    def __init__(self):
        self.logs=[]

    def add(self,event,data):
        self.logs.append({
            "time":datetime.utcnow().isoformat(),
            "event":event,
            "data":data
        })

    def all(self):
        return self.logs

trade_journal=TradeJournal()
