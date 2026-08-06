class AdvancedRiskGovernor:

    def evaluate(self,account,trade):
        balance=account.get("balance",10)
        risk=account.get("risk_percent",1)
        drawdown=account.get("drawdown",0)

        if drawdown>=account.get("max_drawdown",10):
            return {
                "approved":False,
                "reason":"MAX_DRAWDOWN_LIMIT"
            }

        risk_amount=balance*(risk/100)

        return {
            "approved":True,
            "risk_amount":risk_amount,
            "risk_score":100-drawdown
        }


risk_governor=AdvancedRiskGovernor()
