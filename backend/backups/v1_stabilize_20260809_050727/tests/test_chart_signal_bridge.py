from app.integration.chart_signal.chart_signal_bridge import ChartSignalBridge


class MockSignalEngine:
    pass


signal = {
    "decision": "BUY",
    "confidence": 70
}


smart_money = {
    "engine": "SMART_MONEY_SCORE",
    "score": 100,
    "decision": "BUY",
    "reasons": [
        "UPTREND",
        "LIQUIDITY",
        "BULLISH_ORDER_BLOCK",
        "FVG"
    ]
}


structure = {
    "structure": "UPTREND",
    "last_high": 2450,
    "last_low": 2410
}


bridge = ChartSignalBridge(
    MockSignalEngine()
)


result = bridge.enrich(
    signal,
    smart_money,
    structure
)


print("FINAL ENRICHED SIGNAL:")
print(result)
