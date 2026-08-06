from app.chart_ai.structure.market_structure import MarketStructureEngine
from app.chart_ai.smart_money.smart_money_engine import SmartMoneyEngine


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


structure = MarketStructureEngine().analyze(
    candles
)


smart_money = SmartMoneyEngine().analyze(
    structure,
    candles
)


print("STRUCTURE:")
print(structure)

print()

print("SMART MONEY:")
print(smart_money)
