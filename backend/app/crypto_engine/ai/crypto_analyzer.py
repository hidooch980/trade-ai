CRYPTO_RULES={
"BTCUSD":{"risk":1,"volatility":"HIGH"},
"ETHUSD":{"risk":1,"volatility":"HIGH"}
}

class CryptoAI:
    def analyze(self,symbol,price,volume):
        risk=CRYPTO_RULES.get(symbol,{"risk":0.5})
        signal="WAIT"

        if volume>0:
            signal="ANALYZE"

        return {
            "symbol":symbol,
            "price":price,
            "volume":volume,
            "signal":signal,
            "risk":risk
        }

crypto_ai=CryptoAI()
