class AIMarketStreamEngine:

    def __init__(self):
        self.streams=[]
        self.ticks=[]
        self.candles=[]
        self.events=[]


    def connect_stream(self,name):

        stream={
            "source":name,
            "status":"CONNECTED"
        }

        self.streams.append(stream)

        return stream


    def process_tick(self,data):

        self.ticks.append(data)

        return {
            "status":"PROCESSED"
        }


    def process_candle(self,data):

        self.candles.append(data)

        return {
            "status":"PROCESSED"
        }


    def detect_event(self,event):

        self.events.append(event)

        return {
            "event":event,
            "status":"DETECTED"
        }


    def status(self):

        return {
            "streams":len(self.streams),
            "ticks":len(self.ticks),
            "candles":len(self.candles),
            "events":len(self.events),
            "stream":"ONLINE"
        }


market_stream=AIMarketStreamEngine()
