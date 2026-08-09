from app.pipeline.trading_pipeline import TradingPipeline


def mock_signal_engine(data):

    return {
        "decision": "BUY",
        "symbol": data["symbol"],
        "price": data["price"],
        "confidence": 85
    }


def mock_risk_engine(signal):

    return {
        "approved": True,
        "volume": 1.0
    }


def mock_trade_manager(signal):

    return {
        "status": "OPEN",
        "symbol": signal["symbol"],
        "side": signal["decision"],
        "entry": signal["price"]
    }



pipeline = TradingPipeline(
    mock_signal_engine,
    mock_risk_engine,
    mock_trade_manager
)


result = pipeline.execute(
    {
        "symbol": "XAUUSD",
        "price": 2450
    }
)


print("PIPELINE RESULT:")
print(result)
