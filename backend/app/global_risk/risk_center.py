class GlobalRiskCenter:

    def __init__(self):
        self.accounts={}


    def register_account(self,account_id,balance):

        self.accounts[account_id]={
            "balance":balance,
            "risk":0,
            "status":"ACTIVE"
        }

        return self.accounts[account_id]


    def evaluate(self,account_id,trade):

        account=self.accounts.get(account_id)

        if not account:
            return {
                "approved":False,
                "reason":"ACCOUNT_NOT_FOUND"
            }

        risk=trade.get("risk_percent",0)

        account["risk"]=risk

        if risk>2:
            account["status"]="BLOCKED"

            return {
                "approved":False,
                "reason":"HIGH_RISK"
            }

        return {
            "approved":True,
            "risk":risk
        }


    def overview(self):

        return {
            "accounts":len(self.accounts),
            "system":"RISK_ACTIVE"
        }


risk_center=GlobalRiskCenter()
