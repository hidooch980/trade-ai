from typing import List


class IndicatorEngine:

    def sma(self, prices: List[float], period: int = 14):

        if len(prices) < period:
            return None

        return sum(prices[-period:]) / period


    def ema(self, prices: List[float], period: int = 14):

        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema

        return round(ema, 5)


    def rsi(self, prices: List[float], period: int = 14):

        if len(prices) <= period:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):
            diff = prices[i] - prices[i-1]

            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        return round(100 - (100 / (1 + rs)), 2)


    def volatility(self, prices: List[float]):

        if len(prices) < 2:
            return 0

        change = abs(prices[-1] - prices[0])

        return round(
            (change / prices[0]) * 100,
            3
        )
