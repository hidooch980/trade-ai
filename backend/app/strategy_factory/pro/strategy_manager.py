class StrategyManager:

    def __init__(self):
        self.strategies={
            "SMART_MONEY":50,
            "QUANT":50,
            "TREND_FOLLOWING":50,
            "SCALPING":50,
            "BREAKOUT":50,
            "MEAN_REVERSION":50
        }


    def select(self,market):

        regime=market.get("regime")

        if regime=="TREND":
            return "TREND_FOLLOWING"

        if regime=="RANGE":
            return "MEAN_REVERSION"

        if regime=="HIGH_VOLATILITY":
            return "SCALPING"

        return max(
            self.strategies,
            key=self.strategies.get
        )


    def learn(self,name,result):

        if name in self.strategies:

            if result>0:
                self.strategies[name]=min(
                    self.strategies[name]+5,
                    100
                )

            else:
                self.strategies[name]=max(
                    self.strategies[name]-5,
                    0
                )

        return self.strategies


strategy_manager=StrategyManager()
