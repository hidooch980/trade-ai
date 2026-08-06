from app.indicators.volume.vwap import VWAPEngine

candles = [
    {
        "high": 2390,
        "low": 2375,
        "close": 2385,
        "volume": 1000
    },
    {
        "high": 2400,
        "low": 2380,
        "close": 2395,
        "volume": 1200
    },
    {
        "high": 2410,
        "low": 2390,
        "close": 2405,
        "volume": 1500
    }
]


result = VWAPEngine().calculate(
    candles
)

print("VWAP RESULT:")
print(result)
