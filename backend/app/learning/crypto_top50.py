import requests


class CryptoTop50:

    def get_symbols(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": False
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        coins = response.json()

        return [
            {
                "id": c["id"],
                "symbol": c["symbol"].upper(),
                "name": c["name"]
            }
            for c in coins
        ]


crypto_top50 = CryptoTop50()
