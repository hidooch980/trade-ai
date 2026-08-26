"""The risk brain's decisions, from inputs alone."""

from decimal import Decimal

import pytest

from app.risk.brain import (
    AccountSnapshot,
    Decision,
    PositionView,
    ProposedTrade,
    RiskPolicy,
    RuleStatus,
    contract_units,
    risk_brain,
)
from app.risk.brain.core import Rule


def rule(verdict, which: Rule):
    return next(r for r in verdict.rules if r.rule is which)


def flat(equity="10000", **kwargs):
    return AccountSnapshot(
        balance=Decimal(equity), equity=Decimal(equity), **kwargs
    )


# ------------------------------------------------------------------ basics


def test_an_untouched_account_is_allowed():
    verdict = risk_brain.assess(flat())

    assert verdict.decision is Decision.ALLOW
    assert verdict.allowed is True
    assert verdict.breaches == ()
    assert verdict.reasons == ()


def test_every_rule_is_reported_even_when_it_passes():
    verdict = risk_brain.assess(flat())

    reported = {r.rule for r in verdict.rules}
    assert Rule.DAILY_LOSS in reported
    assert Rule.TOTAL_LOSS in reported
    assert Rule.OPEN_POSITIONS in reported
    assert Rule.TOTAL_EXPOSURE in reported
    # TRADE_RISK only applies to a proposed trade.
    assert Rule.TRADE_RISK not in reported


# -------------------------------------------------------------- daily loss


def test_daily_loss_measures_against_the_day_opening_not_the_balance():
    # Balance says 10,000 but the day opened at 12,000 after yesterday's win.
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("11400"),
        day_start_equity=Decimal("12000"),
    )

    result = rule(risk_brain.assess(snapshot), Rule.DAILY_LOSS)

    assert result.used == Decimal("5")
    assert result.status is RuleStatus.BREACH


def test_daily_loss_warns_before_it_blocks():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("9580"),
        day_start_equity=Decimal("10000"),
    )

    verdict = risk_brain.assess(snapshot)

    assert rule(verdict, Rule.DAILY_LOSS).status is RuleStatus.WARN
    assert verdict.decision is Decision.WARN
    assert verdict.allowed is True, "a warning still lets the trade through"


def test_a_profitable_day_uses_no_daily_allowance():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10800"),
        day_start_equity=Decimal("10000"),
    )

    assert rule(risk_brain.assess(snapshot), Rule.DAILY_LOSS).used == Decimal("0")


# ----------------------------------------------------------- total drawdown


def test_drawdown_is_measured_from_the_peak():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("13500"),
        peak_equity=Decimal("15000"),
    )

    result = rule(risk_brain.assess(snapshot), Rule.TOTAL_LOSS)

    assert result.used == Decimal("10")
    assert result.status is RuleStatus.BREACH


def test_a_stale_peak_below_current_equity_is_ignored():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("12000"),
        peak_equity=Decimal("9000"),
    )

    assert rule(risk_brain.assess(snapshot), Rule.TOTAL_LOSS).used == Decimal("0")


# --------------------------------------------------------------- trade risk


def test_a_trade_without_a_stop_is_refused():
    trade = ProposedTrade(
        symbol="EURUSD", side="BUY", volume=Decimal("0.1"), entry_price=Decimal("1.1")
    )

    verdict = risk_brain.assess(flat(), trade=trade)

    result = rule(verdict, Rule.TRADE_RISK)
    assert result.status is RuleStatus.BREACH
    assert result.detail == "NO_STOP_LOSS"
    assert verdict.decision is Decision.BLOCK


def test_trade_risk_uses_the_asset_class_contract_size():
    # 20 pips on 0.1 FX lots is 0.0020 * 0.1 * 100_000 = 20 units of risk,
    # which is 0.2% of a 10,000 account.
    trade = ProposedTrade(
        symbol="EURUSD",
        side="BUY",
        volume=Decimal("0.1"),
        entry_price=Decimal("1.1000"),
        stop_loss=Decimal("1.0980"),
    )

    result = rule(risk_brain.assess(flat(), trade=trade), Rule.TRADE_RISK)

    assert trade.risk_amount == Decimal("20.00000")
    assert result.used == Decimal("0.2")
    assert result.status is RuleStatus.OK


def test_an_oversized_trade_blocks():
    trade = ProposedTrade(
        symbol="EURUSD",
        side="BUY",
        volume=Decimal("1.0"),
        entry_price=Decimal("1.1000"),
        stop_loss=Decimal("1.0800"),
    )

    verdict = risk_brain.assess(flat(), trade=trade)

    assert rule(verdict, Rule.TRADE_RISK).status is RuleStatus.BREACH
    assert verdict.decision is Decision.BLOCK
    assert "TRADE_RISK" in verdict.reasons


def test_contract_units_follow_the_asset_class():
    assert contract_units("EURUSD") == Decimal("100000")
    assert contract_units("XAUUSD") == Decimal("100")
    assert contract_units("BTCUSD") == Decimal("1")
    assert contract_units("") == Decimal("1")


# ----------------------------------------------------------- position count


def test_the_proposed_trade_counts_toward_the_position_limit():
    positions = tuple(
        PositionView(symbol=s, volume=Decimal("0.01"), entry_price=Decimal("1"))
        for s in ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD")
    )
    snapshot = AccountSnapshot(
        balance=Decimal("10000"), equity=Decimal("10000"), positions=positions
    )

    without = risk_brain.assess(snapshot)
    assert rule(without, Rule.OPEN_POSITIONS).status is not RuleStatus.BREACH

    with_trade = risk_brain.assess(
        snapshot,
        trade=ProposedTrade(
            symbol="NZDUSD",
            side="BUY",
            volume=Decimal("0.01"),
            entry_price=Decimal("0.6"),
            stop_loss=Decimal("0.59"),
        ),
    )
    assert rule(with_trade, Rule.OPEN_POSITIONS).status is RuleStatus.BREACH


# --------------------------------------------------------------- exposure


def test_exposure_is_notional_over_equity():
    # 0.5 FX lots at 1.10 is 55,000 notional on 10,000 equity — 5.5x.
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="EURUSD", volume=Decimal("0.5"), entry_price=Decimal("1.10")
            ),
        ),
    )

    result = rule(risk_brain.assess(snapshot), Rule.TOTAL_EXPOSURE)

    assert result.used == Decimal("5.5")
    assert result.status is RuleStatus.OK


def test_leverage_beyond_the_ratio_blocks():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="EURUSD", volume=Decimal("1.5"), entry_price=Decimal("1.10")
            ),
        ),
    )

    verdict = risk_brain.assess(snapshot)

    assert rule(verdict, Rule.TOTAL_EXPOSURE).status is RuleStatus.BREACH
    assert verdict.decision is Decision.BLOCK


def test_current_price_beats_entry_price_for_exposure():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="BTCUSD",
                volume=Decimal("1"),
                entry_price=Decimal("40000"),
                current_price=Decimal("60000"),
            ),
        ),
    )

    assert rule(risk_brain.assess(snapshot), Rule.TOTAL_EXPOSURE).used == Decimal("6")


# ----------------------------------------------------------- concentration


def test_everything_in_one_symbol_is_flagged():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="EURUSD", volume=Decimal("0.2"), entry_price=Decimal("1.10")
            ),
            PositionView(
                symbol="EURUSD", volume=Decimal("0.2"), entry_price=Decimal("1.10")
            ),
        ),
    )

    result = rule(risk_brain.assess(snapshot), Rule.SYMBOL_EXPOSURE)

    assert result.used == Decimal("100")
    assert result.detail == "EURUSD"
    assert result.status is RuleStatus.BREACH


def test_a_spread_book_is_not_flagged():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="EURUSD", volume=Decimal("0.05"), entry_price=Decimal("1.10")
            ),
            PositionView(
                symbol="XAUUSD", volume=Decimal("0.02"), entry_price=Decimal("2400")
            ),
            PositionView(
                symbol="BTCUSD", volume=Decimal("0.08"), entry_price=Decimal("60000")
            ),
        ),
    )

    assert rule(risk_brain.assess(snapshot), Rule.SYMBOL_EXPOSURE).status is RuleStatus.OK


# ------------------------------------------------------------- correlation


def test_too_many_positions_in_one_asset_class():
    positions = tuple(
        PositionView(symbol=s, volume=Decimal("0.01"), entry_price=Decimal("1"))
        for s in ("EURUSD", "GBPUSD", "AUDUSD", "NZDUSD")
    )
    snapshot = AccountSnapshot(
        balance=Decimal("10000"), equity=Decimal("10000"), positions=positions
    )

    result = rule(risk_brain.assess(snapshot), Rule.CORRELATED_POSITIONS)

    assert result.used == Decimal("4")
    assert result.detail == "FOREX"
    assert result.status is RuleStatus.BREACH


# ------------------------------------------------------------------ policy


def test_a_stricter_policy_blocks_what_the_default_allows():
    trade = ProposedTrade(
        symbol="EURUSD",
        side="BUY",
        volume=Decimal("0.1"),
        entry_price=Decimal("1.1000"),
        stop_loss=Decimal("1.0980"),
    )

    assert risk_brain.assess(flat(), trade=trade).decision is Decision.ALLOW

    strict = RiskPolicy(max_risk_per_trade_percent=Decimal("0.1"))
    assert risk_brain.assess(flat(), strict, trade=trade).decision is Decision.BLOCK


def test_a_zero_limit_forbids_the_activity_outright():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("10000"),
        positions=(
            PositionView(
                symbol="EURUSD", volume=Decimal("0.01"), entry_price=Decimal("1.10")
            ),
        ),
    )

    policy = RiskPolicy(max_open_positions=0)

    assert rule(risk_brain.assess(snapshot, policy), Rule.OPEN_POSITIONS).status is (
        RuleStatus.BREACH
    )


@pytest.mark.parametrize("bad", ["", None, "not-a-number", float("nan")])
def test_malformed_numbers_do_not_crash_the_brain(bad):
    snapshot = AccountSnapshot(balance=Decimal("10000"), equity=Decimal("10000"))
    policy = RiskPolicy(max_daily_loss_percent=bad).normalised()

    verdict = risk_brain.assess(snapshot, policy)

    assert verdict.decision in {Decision.ALLOW, Decision.WARN, Decision.BLOCK}


# ----------------------------------------------------------------- headroom


def test_headroom_reports_what_is_left():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("9800"),
        day_start_equity=Decimal("10000"),
    )

    result = rule(risk_brain.assess(snapshot), Rule.DAILY_LOSS)

    assert result.used == Decimal("2")
    assert result.limit == Decimal("5")
    assert result.headroom == Decimal("3")
    assert result.utilisation_percent == Decimal("40")


def test_headroom_never_goes_negative():
    snapshot = AccountSnapshot(
        balance=Decimal("10000"),
        equity=Decimal("9000"),
        day_start_equity=Decimal("10000"),
    )

    assert rule(risk_brain.assess(snapshot), Rule.DAILY_LOSS).headroom == Decimal("0")


def test_concentration_does_not_fire_on_a_single_position():
    """One position is trivially 100% of the book; that is not a finding."""
    trade = ProposedTrade(
        symbol="EURUSD",
        side="BUY",
        volume=Decimal("0.1"),
        entry_price=Decimal("1.1000"),
        stop_loss=Decimal("1.0980"),
    )

    result = rule(risk_brain.assess(flat(), trade=trade), Rule.SYMBOL_EXPOSURE)

    assert result.status is RuleStatus.OK
    assert result.detail == "NOT_APPLICABLE"
