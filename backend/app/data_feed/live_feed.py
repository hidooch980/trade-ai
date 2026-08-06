import time


class LiveMarketFeed:

    def __init__(self):
        self.connected=False
        self.ticks=[]


    def connect(self,source="SIMULATION"):

        self.connected=True

        return {
            "source":source,
            "status":"CONNECTED"
        }


    def add_tick(self,symbol,price,volume):

        tick={
            "symbol":symbol,
            "price":price,
            "volume":volume,
            "time":time.time()
        }

        self.ticks.append(tick)

        return tick


    def latest(self):

        return self.ticks[-1] if self.ticks else None


live_feed=LiveMarketFeed()
