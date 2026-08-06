class ExecutionIntelligence:

    def __init__(self):
        self.orders=[]


    def validate(self,signal,market):

        spread=market.get("spread",0)
        slippage=market.get("slippage",0)

        if spread>signal.get("max_spread",5):
            return {
                "approved":False,
                "reason":"HIGH_SPREAD"
            }

        if slippage>signal.get("max_slippage",3):
            return {
                "approved":False,
                "reason":"HIGH_SLIPPAGE"
            }

        return {
            "approved":True,
            "quality_score":100-(spread+slippage)
        }


    def execute(self,order):

        order["status"]="EXECUTED"
        self.orders.append(order)

        return order


execution_ai=ExecutionIntelligence()
