class AIExecutionEngine:

    def __init__(self):
        self.orders=[]
        self.executions=[]


    def create_order(self,user,broker,data):

        order={
            "user":user,
            "broker":broker,
            "data":data,
            "status":"PENDING"
        }

        self.orders.append(order)

        return order


    def verify_permission(self,user):

        return {
            "user":user,
            "permission":"CHECKED"
        }


    def execute(self,order):

        execution={
            "order":order,
            "status":"SENT_TO_BROKER"
        }

        self.executions.append(execution)

        return execution


    def status(self):

        return {
            "orders":len(self.orders),
            "executions":len(self.executions),
            "engine":"ONLINE"
        }


execution_engine=AIExecutionEngine()
