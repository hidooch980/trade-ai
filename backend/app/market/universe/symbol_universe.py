FOREX = [
    "EURUSD","GBPUSD","USDJPY","USDCHF","AUDUSD","USDCAD","NZDUSD",
    "EURGBP","EURJPY","EURCHF","EURAUD","EURCAD","EURNZD",
    "GBPJPY","GBPCHF","GBPAUD","GBPCAD","GBPNZD",
    "AUDJPY","AUDCHF","AUDCAD","AUDNZD",
    "CADJPY","CHFJPY","NZDJPY",
    "USDTRY","USDZAR","USDMXN","USDNOK","USDSEK","USDSGD","USDHKD",
    "USDPLN","USDHUF","USDCNH",
    "EURTRY","EURZAR","EURPLN","EURSEK","EURNOK","EURDKK","EURHUF",
    "GBPTRY","GBPZAR","GBPNOK","GBPSEK",
    "NOKJPY","SEKJPY","AUDSGD","CADCHF","CADNOK","CADSGD",
    "NZDCHF","NZDCAD","NZDSGD","USDDKK","NOKSEK",
    "USDTHB","USDKRW","USDINR","USDIDR","USDMYR","USDCZK",
    "USDILS","USDBRL","USDRUB","USDCLP"
]

METALS = [
    "XAUUSD","XAGUSD","XPTUSD","XPDUSD"
]

INDICES = [
    "US30","US500","NAS100","US100","GER40","GER30",
    "UK100","FRA40","JPN225","HK50","AUS200"
]

CRYPTO = [
    "BTCUSD","ETHUSD","BNBUSD","SOLUSD","XRPUSD","ADAUSD","DOGEUSD",
    "TRXUSD","AVAXUSD","LINKUSD","DOTUSD","LTCUSD","BCHUSD",
    "XLMUSD","XMRUSD","SHIBUSD","SUIUSD","NEARUSD","UNIUSD",
    "AAVEUSD","ATOMUSD","ETCUSD","HBARUSD","TAOUSD","PAXGUSD"
]

ALIASES = {
    "BTC": "BTCUSD",
    "BITCOIN": "BTCUSD",
    "ETH": "ETHUSD",
    "ETHEREUM": "ETHUSD",
    "BNB": "BNBUSD",
    "BINANCECOIN": "BNBUSD",
    "SOL": "SOLUSD",
    "SOLANA": "SOLUSD",
    "XRP": "XRPUSD",
    "RIPPLE": "XRPUSD",
    "DOGE": "DOGEUSD",
    "TRX": "TRXUSD",
    "AVAX": "AVAXUSD",
    "LINK": "LINKUSD",
    "LTC": "LTCUSD",
    "BCH": "BCHUSD",
    "XLM": "XLMUSD",
    "XMR": "XMRUSD",
    "SHIB": "SHIBUSD",
    "SUI": "SUIUSD",
    "NEAR": "NEARUSD",
    "UNI": "UNIUSD",
    "HBAR": "HBARUSD",
    "TAO": "TAOUSD",
    "XAUT": "PAXGUSD",
    "PAXG": "PAXGUSD",
    "GOLD": "XAUUSD",
    "XAU": "XAUUSD",
    "SILVER": "XAGUSD",
    "XAG": "XAGUSD",
    "US100": "NAS100",
    "US_TECH": "NAS100",
    "SPX": "US500",
    "SP500": "US500",
    "DOW": "US30",
    "DAX": "GER40",
    "FTSE": "UK100",
    "NIKKEI": "JPN225"
}

ALL_SYMBOLS = list(dict.fromkeys(FOREX + METALS + INDICES + CRYPTO))

def canonical(symbol):
    if not symbol:
        return symbol
    s = str(symbol).upper().replace("/", "").replace("-", "").replace("_", "")
    return ALIASES.get(s, s)

def category(symbol):
    s = canonical(symbol)
    if s in FOREX:
        return "FOREX"
    if s in METALS:
        return "METALS"
    if s in INDICES:
        return "INDICES"
    if s in CRYPTO:
        return "CRYPTO"
    return "OTHER"
