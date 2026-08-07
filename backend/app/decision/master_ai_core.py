from app.learning.technical_analyzer import technical_analyzer
from app.learning.smart_money_engine import smart_money_engine
from app.risk.risk_engine import risk_engine


class MasterAICore:


    def decide(
        self,
        symbol,
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


        score = 0
        reasons = []


        # Technical
        if technical.get("signal") == "BUY":
            score += 40
            reasons.append(
                "Technical BUY"
            )

        elif technical.get("signal") == "SELL":
            score -= 40
            reasons.append(
                "Technical SELL"
            )


        # Smart Money
        score += smart.get(
            "score",
            0
        )

        reasons += smart.get(
            "reasons",
            []
        )


        if score >= 50:
            action = "BUY"

        elif score <= -50:
            action = "SELL"

        else:
            action = "WAIT"


        price = technical.get(
            "price",
            0
        )


        risk = risk_engine.calculate(
            balance,
            price,
            abs(score)
        )


        return {
            "symbol": symbol,
            "action": action,
            "score": score,
            "confidence": abs(score),
            "reasons": reasons,
            "risk": risk
        }



master_ai_core = MasterAICore()
