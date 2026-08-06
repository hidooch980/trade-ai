from .base_agent import BaseAgent
from app.market.indicators import IndicatorEngine


class QuantAgent(BaseAgent):

    def __init__(self):
        super().__init__("Quant AI")
        self.indicators = IndicatorEngine()


    async def analyze(self, market_data):

        prices = market_data.get("prices", [])

        if len(prices) < 15:
            return self.result(
                "WAIT",
                50,
                "Not enough market data"
            )

        rsi = self.indicators.rsi(prices)
        sma = self.indicators.sma(prices)
        ema = self.indicators.ema(prices)
        volatility = self.indicators.volatility(prices)

        signal = "WAIT"
        confidence = 60

        current = prices[-1]

        if rsi and rsi < 30 and current > ema:
            signal = "BUY"
            confidence = 75

        elif rsi and rsi > 70 and current < ema:
            signal = "SELL"
            confidence = 75

        return self.result(
            signal,
            confidence,
            {
                "RSI": rsi,
                "SMA": sma,
                "EMA": ema,
                "Volatility": volatility
            }
        )
