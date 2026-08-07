from app.chart_ai.smart_money.fusion.smart_money_fusion import SmartMoneyFusion
from app.smart_money.smart_money_engine import smart_money_engine


class SmartMoneyCore:

    def __init__(self):
        self.chart = SmartMoneyFusion()
        self.market = smart_money_engine


    def analyze(
        self,
        symbol,
        candles,
        structure=None,
        liquidity=None,
        order_block=None,
        fvg=None,
        sweep=None
    ):

        chart_result = self.chart.analyze(
            candles,
            structure or {},
            liquidity or {},
            order_block or {},
            fvg or {},
            sweep or {}
        )


        market_result = self.market.analyze(
            symbol
        )


        score = (
            chart_result.get("score",0)
            +
            market_result.get("score",0)
        )


        if score >= 45:
            decision = "BUY"

        elif score <= -60:
            decision = "SELL"

        else:
            decision = "WAIT"


        return {
            "decision": decision,
            "score": score,
            "chart": chart_result,
            "market": market_result
        }


smart_money_core = SmartMoneyCore()
