from app.learning.technical_analyzer import technical_analyzer
from app.learning.smart_money_engine import smart_money_engine
from app.learning.news_intelligence_engine import news_intelligence_engine
from app.risk.risk_engine import risk_engine


class AITraderCoreV2:


    def decide(
        self,
        symbol,
        currency="USD",
        balance=10000
    ):

        technical = technical_analyzer.calculate(
            symbol
        )


        candles = technical_analyzer.get_candles(
            symbol
        )


        smart = smart_money_engine.analyze(
            candles
        )


        news = news_intelligence_engine.analyze_market_impact(
            currency
        )


        score = 0
        reasons = []


        if technical.get(
            "signal"
        ) == "BUY":

            score += 40
            reasons.append(
                "Technical BUY"
            )


        elif technical.get(
            "signal"
        ) == "SELL":

            score -= 40
            reasons.append(
                "Technical SELL"
            )


        score += smart.get(
            "score",
            0
        )

        reasons += smart.get(
            "reasons",
            []
        )


        score += news.get(
            "news_score",
            0
        )


        if score >= 60:

            action = "BUY"


        elif score <= -60:

            action = "SELL"


        else:

            action = "WAIT"



        risk = risk_engine.calculate(
            balance,
            technical.get(
                "price",
                0
            ),
            abs(score)
        )


        return {

            "symbol": symbol,

            "action": action,

            "score": score,

            "confidence": abs(score),

            "reasons": reasons,

            "news": news,

            "risk": risk

        }



ai_trader_core_v2 = AITraderCoreV2()
