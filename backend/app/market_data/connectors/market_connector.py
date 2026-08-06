from datetime import datetime


class MarketConnector:

    def __init__(self):

        self.connected = False


    def connect(self):

        self.connected = True

        return {
            "status": "CONNECTED",
            "provider": "MARKET_FEED"
        }


    def get_price(
        self,
        symbol
    ):

        if not self.connected:

            return {
                "error": "NOT_CONNECTED"
            }


        return {

            "symbol": symbol,

            "price": 2450.0,

            "timestamp": datetime.now()

        }
