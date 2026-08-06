from app.chart_ai.structure.market_structure import MarketStructureEngine


candles = [
    {
        "high": 2390,
        "low": 2375,
        "close": 2385
    },
    {
        "high": 2405,
        "low": 2385,
        "close": 2400
    },
    {
        "high": 2420,
        "low": 2400,
        "close": 2415
    },
    {
        "high": 2435,
        "low": 2410,
        "close": 2430
    }
]


result = MarketStructureEngine().analyze(
    candles
)


print("MARKET STRUCTURE:")
print(result)
