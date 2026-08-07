import yfinance as yf
from app.learning.market_collector import market_collector


class ForexCandleEngine:

    def get_candles(
        self,
        pair,
        interval="1h",
        period="30d"
    ):

        try:
            symbol = pair + "=X"

            data = yf.download(
                symbol,
                interval=interval,
                period=period,
                progress=False
            )

            if data.empty:
                return 0

            count = 0

            for index, row in data.iterrows():

                market_collector.collect(
                    "FOREX",
                    pair,
                    {
                        "time": str(index),
                        "open": float(row["Open"].iloc[0] if hasattr(row["Open"], "iloc") else row["Open"]),
                        "high": float(row["High"].iloc[0] if hasattr(row["High"], "iloc") else row["High"]),
                        "low": float(row["Low"].iloc[0] if hasattr(row["Low"], "iloc") else row["Low"]),
                        "close": float(row["Close"].iloc[0] if hasattr(row["Close"], "iloc") else row["Close"]),
                        "volume": float(row["Volume"].iloc[0] if hasattr(row["Volume"], "iloc") else row["Volume"])
                    }
                )

                count += 1

            return count

        except Exception as e:
            return {
                "error": str(e)
            }


forex_candle_engine = ForexCandleEngine()
