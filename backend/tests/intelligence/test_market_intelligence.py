"""Market intelligence: fusing several reads into one view."""

from decimal import Decimal

import pytest

from app.market_intelligence import (
    Bias,
    Decision,
    Signal,
    SignalKind,
    market_intelligence,
)


def sig(kind, value, confidence=100, source=""):
    return Signal(
        kind=kind,
        value=Decimal(str(value)),
        confidence=Decimal(str(confidence)),
        source=source,
    )


def view(signals, blockers=(), symbol="EURUSD"):
    return market_intelligence.assess(symbol, signals, blockers)


# --------------------------------------------------------------- the basics


def test_no_signals_is_neutral_not_a_guess():
    result = view([])

    assert result.score == Decimal("50")
    assert result.bias is Bias.NEUTRAL
    assert result.decision is Decision.WAIT
    assert result.confidence == Decimal("0")
    assert "NO_SIGNALS" in result.notes


def test_agreeing_bullish_sources_produce_a_buy():
    result = view(
        [
            sig(SignalKind.TECHNICAL, 80),
            sig(SignalKind.FLOW, 78),
            sig(SignalKind.MACRO, 76),
        ]
    )

    assert result.bias is Bias.STRONG_BULLISH
    assert result.decision is Decision.BUY
    assert result.actionable is True
    assert result.agreement > Decimal("90")


def test_agreeing_bearish_sources_produce_a_sell():
    result = view(
        [
            sig(SignalKind.TECHNICAL, 20),
            sig(SignalKind.FLOW, 22),
            sig(SignalKind.MACRO, 25),
        ]
    )

    assert result.bias is Bias.STRONG_BEARISH
    assert result.decision is Decision.SELL


def test_a_flat_read_waits():
    result = view(
        [sig(SignalKind.TECHNICAL, 50), sig(SignalKind.MACRO, 51)]
    )

    assert result.bias is Bias.NEUTRAL
    assert result.decision is Decision.WAIT
    assert result.actionable is False


# --------------------------------------------------------------- weighting


def test_technical_outweighs_news():
    """Three points of technical against one of news should not tie."""
    result = view(
        [sig(SignalKind.TECHNICAL, 90), sig(SignalKind.NEWS, 10)]
    )

    assert result.score > Decimal("50"), result.score


def test_an_unsure_source_pulls_less():
    confident = view(
        [sig(SignalKind.TECHNICAL, 50), sig(SignalKind.MACRO, 100, confidence=100)]
    )
    unsure = view(
        [sig(SignalKind.TECHNICAL, 50), sig(SignalKind.MACRO, 100, confidence=10)]
    )

    assert unsure.score < confident.score


def test_a_zero_confidence_source_does_not_vote():
    result = view(
        [sig(SignalKind.TECHNICAL, 50), sig(SignalKind.NEWS, 100, confidence=0)]
    )

    assert result.score == Decimal("50")


def test_every_source_at_zero_confidence_yields_no_view():
    result = view(
        [
            sig(SignalKind.TECHNICAL, 90, confidence=0),
            sig(SignalKind.MACRO, 10, confidence=0),
        ]
    )

    assert result.decision is Decision.WAIT
    assert result.confidence == Decimal("0")
    assert "NO_CONFIDENCE" in result.notes


# --------------------------------------------------------------- agreement


def test_a_split_book_is_not_a_trade():
    """One source screaming buy and another screaming sell averages to a lie."""
    result = view(
        [
            sig(SignalKind.TECHNICAL, 95),
            sig(SignalKind.FLOW, 5),
            sig(SignalKind.MACRO, 90),
        ]
    )

    assert result.agreement < Decimal("50")
    assert "SOURCES_DISAGREE" in result.notes
    assert result.decision is not Decision.BUY


def test_agreement_is_high_when_sources_line_up():
    result = view(
        [sig(SignalKind.TECHNICAL, 70), sig(SignalKind.FLOW, 71)]
    )

    assert result.agreement > Decimal("95")


def test_disagreement_discounts_confidence():
    agreeing = view([sig(SignalKind.TECHNICAL, 80), sig(SignalKind.FLOW, 80)])
    arguing = view([sig(SignalKind.TECHNICAL, 80), sig(SignalKind.FLOW, 20)])

    assert arguing.confidence < agreeing.confidence


def test_a_single_source_is_flagged():
    result = view([sig(SignalKind.TECHNICAL, 85)])

    assert "SINGLE_SOURCE" in result.notes
    assert result.decision is Decision.WAIT, "one voice is not a consensus"


# --------------------------------------------------------------- blockers


def test_a_blocker_stands_the_trade_aside_without_moving_the_score():
    clean = view([sig(SignalKind.TECHNICAL, 85), sig(SignalKind.FLOW, 83)])
    blocked = view(
        [sig(SignalKind.TECHNICAL, 85), sig(SignalKind.FLOW, 83)],
        blockers=["NEWS_BLACKOUT"],
    )

    assert clean.decision is Decision.BUY
    assert blocked.decision is Decision.STAND_ASIDE
    assert blocked.score == clean.score, "a blocker is not a bearish opinion"
    assert blocked.bias is clean.bias
    assert blocked.blockers == ("NEWS_BLACKOUT",)


def test_empty_blockers_are_ignored():
    result = view(
        [sig(SignalKind.TECHNICAL, 85), sig(SignalKind.FLOW, 83)],
        blockers=["", "   "],
    )

    assert result.decision is Decision.BUY
    assert result.blockers == ()


# ------------------------------------------------------------ contribution


def test_contribution_names_who_drove_the_view():
    result = view(
        [
            sig(SignalKind.TECHNICAL, 90, source="ema-stack"),
            sig(SignalKind.NEWS, 55, source="headline-scan"),
        ]
    )

    leader = result.leading_source
    assert leader is not None
    assert leader.kind is SignalKind.TECHNICAL
    assert leader.source == "ema-stack"
    assert sum(s.contribution for s in result.sources) == pytest.approx(
        Decimal("100"), abs=Decimal("0.01")
    )


def test_a_neutral_source_contributes_nothing():
    result = view(
        [sig(SignalKind.TECHNICAL, 90), sig(SignalKind.MACRO, 50)]
    )

    macro = next(s for s in result.sources if s.kind is SignalKind.MACRO)
    assert macro.contribution == Decimal("0")


# ------------------------------------------------------------ bad input


@pytest.mark.parametrize("bad", ["", None, "abc", float("nan"), float("inf")])
def test_unusable_values_fall_back_to_neutral(bad):
    result = view([Signal(kind=SignalKind.TECHNICAL, value=bad)])

    assert result.score == Decimal("50")


def test_out_of_range_values_are_clamped_not_rejected():
    high = view([sig(SignalKind.TECHNICAL, 500), sig(SignalKind.FLOW, 500)])
    low = view([sig(SignalKind.TECHNICAL, -500), sig(SignalKind.FLOW, -500)])

    assert high.score == Decimal("100")
    assert low.score == Decimal("0")


def test_the_old_hardcoded_behaviour_is_gone():
    """
    The previous version averaged four constants of 50, so every instrument
    scored 50 and every decision was WAIT. Different inputs must now give
    different answers.
    """
    bullish = view([sig(SignalKind.TECHNICAL, 88), sig(SignalKind.FLOW, 84)])
    bearish = view([sig(SignalKind.TECHNICAL, 12), sig(SignalKind.FLOW, 16)])

    assert bullish.score != bearish.score
    assert bullish.decision is Decision.BUY
    assert bearish.decision is Decision.SELL
