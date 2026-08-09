from app.signals.models.signal import TradingSignal


class SignalGenerator:

    def generate(
        self,
        symbol,
        decision_result,
        risk_result
    ):

        final_decision = risk_result.get(
            "final_decision",
            "WAIT"
        )

        confidence = decision_result.get(
            "confidence",
            0
        )

        reason = {
            "ai": decision_result,
            "risk": risk_result
        }

        return TradingSignal(
            symbol=symbol,
            decision=final_decision,
            confidence=confidence,
            reason=reason,
            risk_status=(
                "APPROVED"
                if risk_result.get("approved")
                else "BLOCKED"
            )
        )
