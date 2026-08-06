from datetime import datetime

class TradeJournal:
    def __init__(self):
        self.entries=[]

    def add(self,data):
        data["time"]=datetime.utcnow().isoformat()
        self.entries.append(data)
        return data

    def all(self):
        return self.entries

trade_journal=TradeJournal()
