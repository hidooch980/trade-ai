from datetime import datetime


class TradingSignal:

    def __init__(
        self,
        symbol,
        decision,
        confidence,
        reason,
        risk_status
    ):

        self.symbol = symbol
        self.decision = decision
        self.confidence = confidence
        self.reason = reason
        self.risk_status = risk_status
        self.created_at = datetime.utcnow()


    def to_dict(self):

        return {
            "symbol": self.symbol,
            "decision": self.decision,
            "confidence": self.confidence,
            "reason": self.reason,
            "risk_status": self.risk_status,
            "created_at": self.created_at
        }
