from app.chart_ai.smart_money.liquidity.liquidity_engine import LiquidityEngine


candles = [
    {
        "high": 2390,
        "low": 2375,
        "close": 2385
    },
    {
        "high": 2410,
        "low": 2385,
        "close": 2405
    },
    {
        "high": 2430,
        "low": 2400,
        "close": 2425
    },
    {
        "high": 2445,
        "low": 2415,
        "close": 2440
    }
]


result = LiquidityEngine().analyze(
    candles
)


print("LIQUIDITY RESULT:")
print(result)
