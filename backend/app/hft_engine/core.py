import time


class HFTEngine:

    def __init__(self):
        self.ticks=[]
        self.orders=[]


    def receive_tick(self,data):

        self.ticks.append({
            "data":data,
            "time":time.time()
        })

        return {
            "received":True
        }


    def optimize_order(self,order):

        return {
            "order":order,
            "execution":"OPTIMIZED",
            "latency":"LOW"
        }


    def status(self):

        return {
            "ticks":len(self.ticks),
            "orders":len(self.orders),
            "engine":"ACTIVE"
        }


hft_engine=HFTEngine()
