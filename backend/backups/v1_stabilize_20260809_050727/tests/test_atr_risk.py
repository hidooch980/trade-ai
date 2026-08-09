from app.risk.atr_risk_calculator import ATRRiskCalculator

calculator = ATRRiskCalculator()

buy_trade = calculator.calculate(
    entry_price=2380,
    atr_value=5,
    direction="BUY",
    atr_multiplier=2,
    reward_ratio=2
)

sell_trade = calculator.calculate(
    entry_price=2380,
    atr_value=5,
    direction="SELL",
    atr_multiplier=2,
    reward_ratio=2
)

print("BUY RISK:", buy_trade)
print("SELL RISK:", sell_trade)
