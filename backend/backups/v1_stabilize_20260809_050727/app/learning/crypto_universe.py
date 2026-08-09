import requests


class CryptoUniverse:

    def get_top200(self):

        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"

            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 200,
                "page": 1
            }

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            coins = response.json()

            return [
                {
                    "id": c["id"],
                    "symbol": c["symbol"].upper()
                }
                for c in coins
            ]

        except Exception:
            return []


crypto_universe = CryptoUniverse()
