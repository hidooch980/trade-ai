class AIComplianceIntelligence:

    def __init__(self):
        self.rules=[]
        self.risk_checks=[]
        self.approved=[]
        self.rejected=[]
        self.audit=[]


    def add_rule(self,rule):

        self.rules.append(rule)


    def check_risk(self,data):

        result={
            "data":data,
            "status":"CHECKED"
        }

        self.risk_checks.append(result)

        return result


    def approve_trade(self,trade):

        self.approved.append(trade)

        return {
            "status":"APPROVED"
        }


    def reject_trade(self,trade,reason):

        self.rejected.append({
            "trade":trade,
            "reason":reason
        })

        return {
            "status":"REJECTED"
        }


    def audit_log(self,item):

        self.audit.append(item)


    def status(self):

        return {
            "rules":len(self.rules),
            "risk_checks":len(self.risk_checks),
            "approved":len(self.approved),
            "rejected":len(self.rejected),
            "compliance":"ONLINE"
        }


compliance=AIComplianceIntelligence()
