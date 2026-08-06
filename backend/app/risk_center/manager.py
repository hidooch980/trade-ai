class AIRiskCenter:

    def __init__(self):
        self.accounts={}


    def register(self,account_id,data):

        self.accounts[account_id]=data

        return {
            "registered":True,
            "account":account_id
        }


    def scan(self):

        warnings=[]

        for account,data in self.accounts.items():

            drawdown=data.get("drawdown",0)

            if drawdown>=10:
                warnings.append({
                    "account":account,
                    "risk":"MAX_DRAWDOWN"
                })

        return {
            "accounts":len(self.accounts),
            "warnings":warnings,
            "status":"SAFE"
            if not warnings else "WARNING"
        }


    def emergency_stop(self,account):

        if account in self.accounts:
            self.accounts[account]["status"]="STOPPED"

        return {
            "account":account,
            "action":"EMERGENCY_STOP"
        }


risk_center=AIRiskCenter()
