from datetime import datetime


class TradeHistory:

    def __init__(self):

        self.trades = []


    def save(
        self,
        trade
    ):

        record = {
            **trade,
            "closed_at": datetime.now()
        }

        self.trades.append(record)

        return record


    def all(self):

        return self.trades
