class AIExecutionEngine:

    def __init__(self):
        self.orders=[]


    def validate(self,order,risk):

        if risk!="SAFE":
            return {
                "approved":False,
                "reason":"RISK_BLOCK"
            }

        return {
            "approved":True
        }


    def execute(self,order):

        result={
            "order":order,
            "status":"EXECUTED",
            "slippage":0
        }

        self.orders.append(result)

        return result


    def history(self):

        return {
            "orders":len(self.orders)
        }


execution_engine=AIExecutionEngine()
