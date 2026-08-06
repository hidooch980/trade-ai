import json
import os
from datetime import datetime

FILE="market_ticks.json"

class MarketStorage:

    def save(self,data):
        items=[]

        if os.path.exists(FILE):
            with open(FILE,"r") as f:
                try:
                    items=json.load(f)
                except:
                    items=[]

        data["time"]=datetime.utcnow().isoformat()
        items.append(data)

        with open(FILE,"w") as f:
            json.dump(items,f,indent=2)

        return data

    def all(self):
        if not os.path.exists(FILE):
            return []

        with open(FILE,"r") as f:
            return json.load(f)

market_storage=MarketStorage()
