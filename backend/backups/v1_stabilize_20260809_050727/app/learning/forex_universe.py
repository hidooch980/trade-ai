class ForexUniverse:

    def get_all_pairs(self):

        return [
            # USD majors
            "EURUSD","GBPUSD","USDJPY","USDCHF","AUDUSD","USDCAD","NZDUSD",

            # EUR crosses
            "EURGBP","EURJPY","EURCHF","EURAUD","EURCAD","EURNZD",
            "EURTRY","EURZAR","EURPLN","EURSEK","EURNOK","EURDKK","EURHUF",

            # GBP crosses
            "GBPJPY","GBPCHF","GBPAUD","GBPCAD","GBPNZD",
            "GBPTRY","GBPZAR","GBPNOK","GBPSEK",

            # JPY crosses
            "AUDJPY","CADJPY","CHFJPY","NZDJPY","NOKJPY","SEKJPY",

            # AUD crosses
            "AUDCAD","AUDCHF","AUDNZD","AUDSGD",

            # CAD crosses
            "CADCHF","CADNOK","CADSGD",

            # NZD crosses
            "NZDCHF","NZDCAD","NZDSGD",

            # Scandinavian
            "USDNOK","USDSEK","USDDKK","NOKSEK",

            # Asian
            "USDSGD","USDHKD","USDCNH","USDTHB",
            "USDKRW","USDINR","USDIDR","USDMYR",

            # Emerging
            "USDTRY","USDZAR","USDMXN","USDPLN",
            "USDHUF","USDCZK","USDILS",
            "USDBRL","USDRUB","USDCLP",

            # Metals
            "XAUUSD","XAGUSD","XPTUSD","XPDUSD",

            # Crypto FX style
            "BTCUSD","ETHUSD"
        ]


forex_universe = ForexUniverse()
