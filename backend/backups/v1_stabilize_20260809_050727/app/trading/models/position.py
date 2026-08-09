from datetime import datetime


class Position:

    def __init__(
        self,
        symbol,
        side,
        entry_price,
        volume,
        stop_loss,
        take_profit
    ):

        self.symbol = symbol
        self.side = side
        self.entry_price = entry_price
        self.volume = volume
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.status = "OPEN"
        self.created_at = datetime.now()


    def to_dict(self):

        return {
            "symbol": self.symbol,
            "side": self.side,
            "entry_price": self.entry_price,
            "volume": self.volume,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "status": self.status,
            "created_at": self.created_at
        }
