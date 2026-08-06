class TradingDigitalTwin:

    def __init__(self):
        self.accounts={}
        self.simulations=[]


    def create_account(self,user,balance):

        self.accounts[user]={
            "balance":balance,
            "equity":balance,
            "trades":[]
        }

        return self.accounts[user]


    def simulate_trade(self,user,trade):

        account=self.accounts.get(user)

        if not account:
            return {
                "error":"ACCOUNT_NOT_FOUND"
            }

        pnl=trade.get("pnl",0)

        account["equity"]+=pnl
        account["trades"].append(trade)

        return {
            "user":user,
            "equity":account["equity"],
            "pnl":pnl
        }


    def scenario(self,name):

        result={
            "scenario":name,
            "status":"SIMULATED"
        }

        self.simulations.append(result)

        return result


digital_twin=TradingDigitalTwin()
