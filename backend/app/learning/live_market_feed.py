import requests
from app.learning.market_collector import market_collector
from app.learning.crypto_top50 import crypto_top50


class LiveMarketFeed:

    def collect_top50_crypto(self):

        coins = crypto_top50.get_symbols()

        ids = ",".join(
            [coin["id"] for coin in coins]
        )

        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": ids,
            "vs_currencies": "usd",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        data = response.json()

        for coin in coins:
            info = data.get(coin["id"])

            if info:
                market_collector.collect(
                    "CRYPTO",
                    coin["symbol"],
                    {
                        "price": info.get("usd"),
                        "volume": info.get("usd_24h_vol"),
                        "change_24h": info.get("usd_24h_change")
                    }
                )

        return {
            "collected": len(data)
        }


live_market_feed = LiveMarketFeed()
