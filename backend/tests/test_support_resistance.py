from app.chart_ai.levels.support_resistance import SupportResistanceEngine


candles = [
    {
        "high": 2390,
        "low": 2375,
        "close": 2385
    },
    {
        "high": 2405,
        "low": 2380,
        "close": 2398
    },
    {
        "high": 2420,
        "low": 2395,
        "close": 2410
    },
    {
        "high": 2415,
        "low": 2388,
        "close": 2400
    },
    {
        "high": 2430,
        "low": 2405,
        "close": 2425
    }
]


result = SupportResistanceEngine().analyze(
    candles
)


print("SUPPORT RESISTANCE:")
print(result)
