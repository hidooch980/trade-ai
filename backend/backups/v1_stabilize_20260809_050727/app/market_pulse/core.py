class AIMarketPulseEngine:

    def __init__(self):
        self.streams=[]
        self.changes=[]
        self.events=[]
        self.alerts=[]


    def receive_data(self,source,data):

        item={
            "source":source,
            "data":data
        }

        self.streams.append(item)

        return item


    def detect_change(self,market,change):

        item={
            "market":market,
            "change":change
        }

        self.changes.append(item)

        return item


    def analyze_event(self,event,impact):

        item={
            "event":event,
            "impact":impact
        }

        self.events.append(item)

        return item


    def create_alert(self,message):

        self.alerts.append(message)

        return {
            "status":"CREATED"
        }


    def status(self):

        return {
            "streams":len(self.streams),
            "changes":len(self.changes),
            "events":len(self.events),
            "alerts":len(self.alerts),
            "pulse":"ONLINE"
        }


market_pulse=AIMarketPulseEngine()
