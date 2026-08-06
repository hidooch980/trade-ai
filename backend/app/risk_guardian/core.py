class AIRiskGuardian:

    def __init__(self):
        self.checks=[]
        self.blocks=[]
        self.alerts=[]
        self.actions=[]


    def analyze_risk(self,data):

        check={
            "data":data,
            "status":"ANALYZED"
        }

        self.checks.append(check)

        return check


    def approve_trade(self,trade):

        item={
            "trade":trade,
            "status":"APPROVED"
        }

        self.actions.append(item)

        return item


    def block_trade(self,reason):

        item={
            "reason":reason,
            "status":"BLOCKED"
        }

        self.blocks.append(item)

        return item


    def create_alert(self,message):

        self.alerts.append(message)

        return {
            "status":"ALERT_CREATED"
        }


    def status(self):

        return {
            "checks":len(self.checks),
            "blocks":len(self.blocks),
            "alerts":len(self.alerts),
            "actions":len(self.actions),
            "risk_guardian":"ONLINE"
        }


risk_guardian=AIRiskGuardian()
