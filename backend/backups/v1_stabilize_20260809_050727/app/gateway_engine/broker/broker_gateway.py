class BrokerGateway:

    def __init__(self):
        self.brokers={
            "MT5":{
                "status":"DEMO",
                "spread":0,
                "latency":0
            }
        }

    def register(self,name,data):
        self.brokers[name]=data
        return self.brokers[name]

    def best_broker(self):
        available=[
            (name,data)
            for name,data in self.brokers.items()
            if data.get("status")!="OFFLINE"
        ]

        if not available:
            return None

        return min(
            available,
            key=lambda x:x[1].get("spread",999)
        )

    def status(self):
        return self.brokers


broker_gateway=BrokerGateway()
