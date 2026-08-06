from app.signals.models.signal import TradingSignal
from app.signals.history.signal_history import SignalHistory


history = SignalHistory()


signal = TradingSignal(
    symbol="XAUUSD",
    decision="BUY",
    confidence=78,
    reason={
        "source": "AI Committee"
    },
    risk_status="APPROVED"
)


saved = history.save(
    signal
)


print("SAVED SIGNAL:")
print(saved)


updated = history.update_result(
    0,
    "WIN"
)


print("UPDATED RESULT:")
print(updated)


print("ALL HISTORY:")
print(history.all())
