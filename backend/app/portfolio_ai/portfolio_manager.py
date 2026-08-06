class PortfolioManager:

    def __init__(self):
        self.positions=[]


    def add_position(self,position):
        self.positions.append(position)
        return position


    def exposure(self):

        total=0

        for p in self.positions:
            total+=p.get("risk",0)

        return {
            "total_risk":total,
            "positions":len(self.positions)
        }


    def check_limit(self,max_risk=5):

        current=self.exposure()["total_risk"]

        if current>=max_risk:
            return {
                "approved":False,
                "reason":"PORTFOLIO_RISK_LIMIT"
            }

        return {
            "approved":True,
            "risk":current
        }


portfolio_manager=PortfolioManager()
