import csv
from app.market_data.models.candle import Candle
from datetime import datetime

class CSVMarketLoader:

    def load(self, path):
        candles = []

        with open(path, newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                candles.append(
                    Candle(
                        symbol=row["symbol"],
                        timeframe=row["timeframe"],
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row.get("volume",0)),
                        timestamp=datetime.fromisoformat(row["timestamp"])
                    )
                )

        return candles
