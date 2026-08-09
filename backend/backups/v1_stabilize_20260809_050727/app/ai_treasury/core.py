class AITreasuryManager:

    def __init__(self):
        self.capitals=[]
        self.liquidity=[]
        self.reserves=[]
        self.allocations=[]

    def register_capital(self,item):
        self.capitals.append(item)

    def manage_liquidity(self,item):
        self.liquidity.append(item)

    def create_reserve(self,item):
        self.reserves.append(item)

    def allocate(self,item):
        self.allocations.append(item)

    def status(self):
        return {
            "capitals":len(self.capitals),
            "liquidity":len(self.liquidity),
            "reserves":len(self.reserves),
            "allocations":len(self.allocations),
            "treasury":"ONLINE"
        }


ai_treasury=AITreasuryManager()
