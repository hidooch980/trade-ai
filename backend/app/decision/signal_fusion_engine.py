from app.learning.technical_analyzer import technical_analyzer


class SignalFusionEngine:


    def analyze(self, symbol):

        technical = technical_analyzer.calculate(symbol)

        score = 0
        reasons = []


        signal = technical.get("signal")


        if signal == "BUY":
            score += 40
            reasons.append(
                "Technical BUY"
            )


        elif signal == "SELL":
            score -= 40
            reasons.append(
                "Technical SELL"
            )


        rsi = technical.get("rsi",50)


        if rsi < 30:
            score += 25
            reasons.append(
                "RSI oversold"
            )


        elif rsi > 70:
            score -= 25
            reasons.append(
                "RSI overbought"
            )


        sma = technical.get("sma20")
        price = technical.get("price")


        if price and sma:

            if price > sma:
                score += 20
                reasons.append(
                    "Above SMA20"
                )

            else:
                score -= 20
                reasons.append(
                    "Below SMA20"
                )


        if score >= 40:
            decision = "BUY"

        elif score <= -40:
            decision = "SELL"

        else:
            decision = "HOLD"


        return {
            "symbol": symbol,
            "decision": decision,
            "score": score,
            "confidence": abs(score),
            "reasons": reasons,
            "technical": technical
        }



signal_fusion_engine = SignalFusionEngine()
