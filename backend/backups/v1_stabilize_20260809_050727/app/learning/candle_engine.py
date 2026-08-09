import requests
from datetime import datetime
from app.learning.market_collector import market_collector


class CandleEngine:

    def get_candles(
        self,
        symbol,
        market="CRYPTO",
        interval="1h"
    ):

        try:

            if market == "CRYPTO":

                url = (
                    "https://api.binance.com/api/v3/klines"
                    f"?symbol={symbol.upper()}USDT"
                    f"&interval={interval}"
                    "&limit=100"
                )

                response = requests.get(
                    url,
                    timeout=10
                )

                candles = response.json()

                for c in candles:

                    market_collector.collect(
                        market,
                        symbol,
                        {
                            "time": datetime.fromtimestamp(
                                c[0] / 1000
                            ).isoformat(),

                            "open": float(c[1]),
                            "high": float(c[2]),
                            "low": float(c[3]),
                            "close": float(c[4]),
                            "volume": float(c[5])
                        }
                    )

                return len(candles)

            return 0

        except Exception as e:
            return {
                "error": str(e)
            }


candle_engine = CandleEngine()
