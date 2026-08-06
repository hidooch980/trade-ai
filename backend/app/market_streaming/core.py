class AIMarketStreaming:

    def __init__(self):
        self.connections=[]
        self.ticks=[]
        self.candles=[]
        self.orderbooks=[]

    def connect_market(self,name):
        item={
            "market":name,
            "status":"CONNECTED"
        }
        self.connections.append(item)
        return item

    def receive_tick(self,data):
        self.ticks.append(data)

    def create_candle(self,data):
        self.candles.append(data)

    def update_orderbook(self,data):
        self.orderbooks.append(data)

    def status(self):
        return {
            "connections":len(self.connections),
            "ticks":len(self.ticks),
            "candles":len(self.candles),
            "orderbooks":len(self.orderbooks),
            "stream":"ONLINE"
        }


market_streaming = AIMarketStreaming()
