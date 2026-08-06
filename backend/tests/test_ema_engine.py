from app.indicators.trend.ema import EMAEngine

prices = [
    2370, 2375, 2380, 2382, 2385,
    2388, 2390, 2395, 2398, 2400,
    2405, 2410, 2412, 2415, 2420,
    2425, 2430, 2435, 2440, 2445,
    2450
]

engine = EMAEngine()

result = engine.calculate(
    prices,
    short_period=9,
    long_period=21
)

print("EMA RESULT:")
print(result)
