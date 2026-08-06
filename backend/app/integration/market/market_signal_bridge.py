class MarketSignalBridge:

    def __init__(
        self,
        indicator_engine
    ):

        self.indicator_engine = indicator_engine


    def analyze(
        self,
        market_data
    ):

        price = market_data.get(
            "price"
        )


        return {

            "symbol": market_data.get(
                "symbol"
            ),

            "price": price,

            "status": "READY_FOR_ANALYSIS"

        }
