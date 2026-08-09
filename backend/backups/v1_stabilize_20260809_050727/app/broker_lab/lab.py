class BrokerTestingLab:

    def __init__(self):
        self.brokers=[]


    def add_broker(self,name,platform):

        broker={
            "name":name,
            "platform":platform,
            "status":"DEMO_READY"
        }

        self.brokers.append(broker)
        return broker


    def test_connection(self,name):

        return {
            "broker":name,
            "connection":"TESTED"
        }


    def status(self):

        return {
            "brokers":len(self.brokers),
            "lab":"ONLINE"
        }


broker_lab=BrokerTestingLab()
