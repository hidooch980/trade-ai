import yfinance as yf
from app.learning.market_collector import market_collector
from app.learning.forex_universe import forex_universe


class ForexBatchFeed:

    def __init__(self):
        self.pairs = forex_universe.get_all_pairs()


    def collect(self):

        count = 0
        failed = 0

        for pair in self.pairs:

            try:
                symbol = pair + "=X"

                data = yf.Ticker(symbol).history(
                    period="1d"
                )

                if not data.empty:

                    price = float(
                        data["Close"].iloc[-1]
                    )

                    market_collector.collect(
                        "FOREX",
                        pair,
                        {
                            "price": price
                        }
                    )

                    count += 1

                else:
                    failed += 1

            except Exception:
                failed += 1
                continue


        return {
            "total": len(self.pairs),
            "collected": count,
            "failed": failed
        }


forex_batch_feed = ForexBatchFeed()
