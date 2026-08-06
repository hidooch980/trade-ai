from app.chart_ai.structure.market_structure import MarketStructureEngine
from app.chart_ai.smart_money.liquidity.liquidity_engine import LiquidityEngine
from app.chart_ai.smart_money.order_block.order_block_engine import OrderBlockEngine
from app.chart_ai.smart_money.fvg.fvg_engine import FVGEngine


candles = [
    {
        "high": 2390,
        "low": 2375,
        "close": 2380
    },
    {
        "high": 2400,
        "low": 2385,
        "close": 2395
    },
    {
        "high": 2420,
        "low": 2400,
        "close": 2415
    },
    {
        "high": 2450,
        "low": 2410,
        "close": 2445
    }
]


structure = MarketStructureEngine().analyze(
    candles
)

liquidity = LiquidityEngine().analyze(
    candles
)

order_block = OrderBlockEngine().analyze(
    candles
)

fvg = FVGEngine().analyze(
    candles
)


print("STRUCTURE:")
print(structure)

print()

print("LIQUIDITY:")
print(liquidity)

print()

print("ORDER BLOCK:")
print(order_block)

print()

print("FVG:")
print(fvg)
