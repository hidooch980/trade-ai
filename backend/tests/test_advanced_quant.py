from app.indicators.trend.ema import EMAEngine
from app.indicators.momentum.rsi import RSIEngine
from app.indicators.momentum.macd import MACDEngine
from app.indicators.core.advanced_quant_signal import AdvancedQuantSignalEngine


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


ema = EMAEngine().calculate(
    prices,
    short_period=9,
    long_period=21
)

rsi = RSIEngine().calculate(
    prices,
    period=14
)

macd = MACDEngine().calculate(
    prices
)


signal = AdvancedQuantSignalEngine().analyze(
    ema,
    rsi,
    macd
)


print("EMA:", ema)
print("RSI:", rsi)
print("MACD:", macd)
print("ADVANCED QUANT:", signal)
