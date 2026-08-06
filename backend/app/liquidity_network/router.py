class LiquidityNetwork:

    def __init__(self):
        self.providers={}
        self.routes=[]


    def add_provider(self,name,score):

        self.providers[name]={
            "score":score,
            "status":"ACTIVE"
        }

        return self.providers[name]


    def select_best(self):

        if not self.providers:
            return None

        return max(
            self.providers,
            key=lambda x:self.providers[x]["score"]
        )


    def route_order(self,order):

        provider=self.select_best()

        route={
            "order":order,
            "provider":provider,
            "status":"ROUTED"
        }

        self.routes.append(route)

        return route


    def status(self):

        return {
            "providers":len(self.providers),
            "routes":len(self.routes),
            "network":"ACTIVE"
        }


liquidity_network=LiquidityNetwork()
