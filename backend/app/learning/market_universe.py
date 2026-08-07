class MarketUniverse:

    def get_assets(self):

        return [

            # Forex Majors
            "EURUSD","GBPUSD","USDJPY","USDCHF","AUDUSD","USDCAD","NZDUSD",

            # Forex Crosses
            "EURGBP","EURJPY","EURCHF","EURAUD","EURCAD","EURNZD",
            "GBPJPY","GBPCHF","GBPAUD","GBPCAD","GBPNZD",
            "AUDJPY","AUDCHF","AUDCAD","AUDNZD",
            "CADJPY","CHFJPY","NZDJPY",

            # Forex Exotic
            "USDTRY","USDZAR","USDMXN","USDNOK","USDSEK",
            "USDSGD","USDHKD","USDPLN","USDHUF","USDCNH",

            # Commodities
            "XAUUSD","XAGUSD","WTI","BRENT",

            # Crypto Major
            "BTC","ETH","BNB","SOL","XRP","ADA","DOGE",
            "AVAX","DOT","LINK","MATIC","LTC","BCH",

            # Indices
            "SPX","NDX","DJI","DAX","FTSE",
            "N225","HSI",

            # Stocks (AI watchlist)
            "AAPL","MSFT","NVDA","TSLA",
            "AMZN","GOOG","META","AMD",
            "NFLX","INTC"

        ]


market_universe = MarketUniverse()
