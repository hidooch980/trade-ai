from app.risk.risk_governor import RiskGovernor


risk = RiskGovernor()


position = risk.calculate_position_size(
    capital=10000,
    risk_percent=2,
    entry_price=2450,
    stop_loss=2430
)


drawdown = risk.validate_drawdown(
    current_loss_percent=3
)


print("POSITION RISK:")
print(position)

print()

print("DRAWDOWN CHECK:")
print(drawdown)
