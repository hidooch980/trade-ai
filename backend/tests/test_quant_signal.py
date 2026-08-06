from app.indicators.trend.ema import EMAEngine
from app.indicators.momentum.rsi import RSIEngine
from app.indicators.core.quant_signal import QuantSignalEngine

prices = [
    2370, 2375, 2380, 2382, 2385,
    2388, 2390, 2395, 2398, 2400,
    2405, 2410, 2412, 2415, 2420,
    2425, 2430, 2435, 2440, 2445,
    2450
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

signal = QuantSignalEngine().analyze(
    ema,
    rsi
)

print("EMA:", ema)
print("RSI:", rsi)
print("QUANT SIGNAL:", signal)
