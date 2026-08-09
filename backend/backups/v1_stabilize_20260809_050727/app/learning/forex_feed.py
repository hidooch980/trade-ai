import yfinance as yf
from app.learning.market_collector import market_collector
from app.learning.forex_universe import forex_universe


class ForexFeed:

    def __init__(self):
        self.pairs = forex_universe.get_all_pairs()

    def collect(self):

        count = 0

        for pair in self.pairs:

            try:
                symbol = pair + "=X"

                ticker = yf.Ticker(symbol)

                data = ticker.history(
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

            except Exception:
                continue

        return {
            "collected": count
        }


forex_feed = ForexFeed()
