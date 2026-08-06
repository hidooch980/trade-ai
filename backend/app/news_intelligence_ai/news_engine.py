class NewsIntelligenceAI:

    def __init__(self):
        self.high_impact=[
            "NFP",
            "CPI",
            "FOMC",
            "INTEREST_RATE",
            "GDP"
        ]


    def analyze(self,event):

        if event in self.high_impact:
            return {
                "impact":"HIGH",
                "trade_allowed":False,
                "reason":"HIGH_IMPACT_EVENT"
            }

        return {
            "impact":"LOW",
            "trade_allowed":True,
            "reason":"NORMAL"
        }


    def risk_adjustment(self,event):

        result=self.analyze(event)

        if not result["trade_allowed"]:
            return 0

        return 100


news_ai=NewsIntelligenceAI()
