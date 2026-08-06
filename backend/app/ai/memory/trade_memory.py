from datetime import datetime


class TradeMemory:


    def __init__(self):

        self.records = []



    def store(self, trade):

        trade["timestamp"] = (
            datetime.utcnow()
            .isoformat()
        )

        self.records.append(
            trade
        )

        return trade



    def history(self):

        return self.records



    def analyze_performance(self):

        total = len(
            self.records
        )

        wins = len(
            [
                x for x in self.records
                if x.get("result") == "WIN"
            ]
        )


        return {

            "total_trades": total,

            "win_rate":
                round(
                    (wins / total) * 100,
                    2
                )
                if total else 0
        }
