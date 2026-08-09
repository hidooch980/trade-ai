class PortfolioManager:

    def __init__(self):
        self.accounts=[]


    def add_account(self,account):
        self.accounts.append(account)
        return account


    def allocate(self,total_capital,strategies):

        if not strategies:
            return {}

        allocation={}

        share=round(
            total_capital/len(strategies),
            2
        )

        for strategy in strategies:
            allocation[strategy]=share

        return allocation


    def risk_report(self):

        exposure=0

        for account in self.accounts:
            exposure+=account.get("exposure",0)

        return {
            "accounts":len(self.accounts),
            "total_exposure":exposure,
            "status":"SAFE" if exposure<50 else "WARNING"
        }


portfolio_manager=PortfolioManager()
