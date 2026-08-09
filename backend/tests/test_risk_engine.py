from app.risk.risk_governor import RiskGovernor
from app.risk.risk_manager import risk_manager


def test_volume():

    governor = RiskGovernor()

    result = governor.calculate_position_size(
        capital=10000,
        risk_percent=2,
        entry_price=115000,
        stop_loss=114000,
        symbol="BTCUSDT"
    )

    print("POSITION SIZE:")
    print(result)


def test_exposure():

    positions = [
        {
            "volume":10,
            "entry_price":100000,
            "pnl":0
        }
    ]

    result = risk_manager.check(
        positions,
        10,
        100000
    )

    print("EXPOSURE CHECK:")
    print(result)


if __name__ == "__main__":

    test_volume()
    test_exposure()
