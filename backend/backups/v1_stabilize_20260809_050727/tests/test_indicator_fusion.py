from app.indicators.trend.ema import EMAEngine
from app.indicators.momentum.rsi import RSIEngine
from app.indicators.momentum.macd import MACDEngine
from app.indicators.volatility.atr import ATREngine
from app.indicators.volume.vwap import VWAPEngine
from app.indicators.core.indicator_fusion import IndicatorFusionEngine


prices = [
    2370,2375,2380,2382,2385,
    2388,2390,2395,2398,2400,
    2405,2410,2412,2415,2420,
    2425,2430,2435,2440,2445,
    2450,2455,2460,2465,2470,
    2475,2480,2485,2490,2495,
    2500,2505,2510,2515,2520,
    2525
]


candles = [
    {
        "high": p + 5,
        "low": p - 5,
        "close": p,
        "volume": 1000 + i * 100
    }
    for i, p in enumerate(prices)
]


ema = EMAEngine().calculate(prices)

rsi = RSIEngine().calculate(prices)

macd = MACDEngine().calculate(prices)

atr = ATREngine().calculate(
    candles
)

vwap = VWAPEngine().calculate(
    candles
)


result = IndicatorFusionEngine().analyze(
    ema,
    rsi,
    macd,
    atr,
    vwap
)

print("EMA:", ema)
print("RSI:", rsi)
print("MACD:", macd)
print("ATR:", atr)
print("VWAP:", vwap)
print("FUSION:", result)
