from datetime import datetime


class SignalHistory:

    def __init__(self):
        self.records = []


    def save(self, signal):

        record = {
            "symbol": signal.symbol,
            "decision": signal.decision,
            "confidence": signal.confidence,
            "risk_status": signal.risk_status,
            "created_at": signal.created_at,
            "result": None
        }

        self.records.append(record)

        return record


    def update_result(
        self,
        index,
        result
    ):

        if index < len(self.records):

            self.records[index]["result"] = result

            return self.records[index]

        return None


    def all(self):

        return self.records
