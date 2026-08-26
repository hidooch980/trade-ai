"""
Market intelligence.

Fuses several independently-sourced reads on one instrument into a single
graded view: which way, how strongly, how much of that is agreement rather
than one loud source, and what would change the answer.

Replaces a version that averaged four constants — every score was hardcoded
to 50, so it returned 50 for every instrument and decided WAIT every time.

Like the risk brain, this reads nothing: no database, no feed, no clock. A
view is reproducible from the signals it was given, which is what lets you
argue with it afterwards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import Enum

ZERO = Decimal("0")
HUNDRED = Decimal("100")
NEUTRAL = Decimal("50")


def score(value) -> Decimal:
    """
    A 0–100 score, clamped.

    Out-of-range input is clamped rather than rejected: a source that reports
    120 means "as bullish as it gets", and refusing the whole view over one
    over-eager input loses more than it protects.
    """
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return NEUTRAL

    if not value.is_finite():
        return NEUTRAL

    return min(HUNDRED, max(ZERO, value))


def weight(value) -> Decimal:
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return ZERO

    return max(ZERO, value) if value.is_finite() else ZERO


class SignalKind(str, Enum):
    TECHNICAL = "TECHNICAL"
    SENTIMENT = "SENTIMENT"
    MACRO = "MACRO"
    NEWS = "NEWS"
    LIQUIDITY = "LIQUIDITY"
    FLOW = "FLOW"


class Bias(str, Enum):
    STRONG_BULLISH = "STRONG_BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    STRONG_BEARISH = "STRONG_BEARISH"


class Decision(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"
    STAND_ASIDE = "STAND_ASIDE"


#: How much each kind of read counts. Technical and flow are what the market
#: is doing; sentiment and news are what people say about it, and are
#: deliberately worth less.
DEFAULT_WEIGHTS: dict[SignalKind, Decimal] = {
    SignalKind.TECHNICAL: Decimal("3"),
    SignalKind.FLOW: Decimal("2.5"),
    SignalKind.LIQUIDITY: Decimal("2"),
    SignalKind.MACRO: Decimal("2"),
    SignalKind.SENTIMENT: Decimal("1.5"),
    SignalKind.NEWS: Decimal("1"),
}


@dataclass(frozen=True)
class Signal:
    """
    One source's read.

    `value` is 0–100 where 50 is no opinion. `confidence` is how much the
    source trusts its own read, also 0–100; a source that is unsure pulls the
    fused score toward neutral instead of voting at full strength.
    """

    kind: SignalKind
    value: Decimal
    confidence: Decimal = HUNDRED
    source: str = ""
    note: str = ""

    @property
    def clean_value(self) -> Decimal:
        return score(self.value)

    @property
    def clean_confidence(self) -> Decimal:
        return score(self.confidence)

    @property
    def effective_weight(self) -> Decimal:
        base = DEFAULT_WEIGHTS.get(self.kind, Decimal("1"))
        return base * self.clean_confidence / HUNDRED

    @property
    def pull(self) -> Decimal:
        """Distance from neutral, signed. Positive is bullish."""
        return self.clean_value - NEUTRAL


@dataclass(frozen=True)
class SourceWeight:
    kind: SignalKind
    value: Decimal
    confidence: Decimal
    weight: Decimal
    #: Share of the final score this source is responsible for, 0–100.
    contribution: Decimal
    source: str = ""
    note: str = ""


@dataclass(frozen=True)
class MarketView:
    symbol: str
    score: Decimal
    bias: Bias
    decision: Decision
    #: How much the sources agree, 0–100. Low agreement means the score is an
    #: average of an argument, not a consensus.
    agreement: Decimal
    confidence: Decimal
    sources: tuple[SourceWeight, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def actionable(self) -> bool:
        return self.decision in (Decision.BUY, Decision.SELL)

    @property
    def leading_source(self) -> SourceWeight | None:
        return max(self.sources, key=lambda s: s.contribution, default=None)


class MarketIntelligence:
    """Turns a bag of signals into one view you can act on or argue with."""

    #: Score thresholds for the bias ladder.
    STRONG = Decimal("72")
    LEAN = Decimal("58")

    #: Below this, the sources disagree too much for the score to mean much.
    MIN_AGREEMENT = Decimal("45")
    #: Below this, nothing has a strong enough opinion to act on.
    MIN_CONFIDENCE = Decimal("35")

    def _bias(self, value: Decimal) -> Bias:
        if value >= self.STRONG:
            return Bias.STRONG_BULLISH
        if value >= self.LEAN:
            return Bias.BULLISH
        if value <= HUNDRED - self.STRONG:
            return Bias.STRONG_BEARISH
        if value <= HUNDRED - self.LEAN:
            return Bias.BEARISH
        return Bias.NEUTRAL

    def _agreement(self, signals: tuple[Signal, ...], fused: Decimal) -> Decimal:
        """
        100 when every source says the same thing, 0 when they are as far
        apart as they can be. Weighted, so a confident technical read
        disagreeing costs more than an unsure news read disagreeing.
        """
        total_weight = sum((s.effective_weight for s in signals), ZERO)

        if total_weight <= ZERO:
            return ZERO

        spread = sum(
            (abs(s.clean_value - fused) * s.effective_weight for s in signals), ZERO
        ) / total_weight

        # Mean absolute deviation maxes out at 50 on a 0–100 scale.
        return max(ZERO, HUNDRED - (spread * 2))

    def assess(
        self,
        symbol: str,
        signals: list[Signal] | tuple[Signal, ...],
        blockers: list[str] | tuple[str, ...] = (),
    ) -> MarketView:
        """
        `blockers` are hard reasons not to trade regardless of the read — a
        news blackout, a closed session. They do not move the score; they stop
        it becoming an instruction, which is a different thing and is reported
        separately.
        """
        signals = tuple(signals)
        blockers = tuple(str(b) for b in blockers if str(b).strip())

        if not signals:
            return MarketView(
                symbol=symbol,
                score=NEUTRAL,
                bias=Bias.NEUTRAL,
                decision=Decision.WAIT,
                agreement=ZERO,
                confidence=ZERO,
                blockers=blockers,
                notes=("NO_SIGNALS",),
            )

        total_weight = sum((s.effective_weight for s in signals), ZERO)

        if total_weight <= ZERO:
            # Every source reported zero confidence.
            return MarketView(
                symbol=symbol,
                score=NEUTRAL,
                bias=Bias.NEUTRAL,
                decision=Decision.WAIT,
                agreement=ZERO,
                confidence=ZERO,
                sources=tuple(
                    SourceWeight(
                        kind=s.kind,
                        value=s.clean_value,
                        confidence=s.clean_confidence,
                        weight=ZERO,
                        contribution=ZERO,
                        source=s.source,
                        note=s.note,
                    )
                    for s in signals
                ),
                blockers=blockers,
                notes=("NO_CONFIDENCE",),
            )

        fused = sum(
            (s.clean_value * s.effective_weight for s in signals), ZERO
        ) / total_weight

        agreement = self._agreement(signals, fused)

        # Confidence is the weighted average of what the sources claim,
        # discounted by how much they disagree — a loud argument is not
        # evidence.
        claimed = sum(
            (s.clean_confidence * s.effective_weight for s in signals), ZERO
        ) / total_weight
        confidence = claimed * agreement / HUNDRED

        bias = self._bias(fused)

        notes: list[str] = []

        if agreement < self.MIN_AGREEMENT:
            notes.append("SOURCES_DISAGREE")
        if confidence < self.MIN_CONFIDENCE:
            notes.append("LOW_CONFIDENCE")
        if len(signals) < 2:
            notes.append("SINGLE_SOURCE")

        if blockers:
            decision = Decision.STAND_ASIDE
        elif notes and bias is not Bias.NEUTRAL:
            # A directional read nobody agrees on is not a trade.
            decision = Decision.WAIT
        elif bias in (Bias.STRONG_BULLISH, Bias.BULLISH):
            decision = Decision.BUY
        elif bias in (Bias.STRONG_BEARISH, Bias.BEARISH):
            decision = Decision.SELL
        else:
            decision = Decision.WAIT

        sources = tuple(
            SourceWeight(
                kind=s.kind,
                value=s.clean_value,
                confidence=s.clean_confidence,
                weight=s.effective_weight,
                contribution=(
                    abs(s.pull) * s.effective_weight
                    / max(
                        sum((abs(x.pull) * x.effective_weight for x in signals), ZERO),
                        Decimal("0.000001"),
                    )
                    * HUNDRED
                ),
                source=s.source,
                note=s.note,
            )
            for s in signals
        )

        return MarketView(
            symbol=symbol,
            score=fused,
            bias=bias,
            decision=decision,
            agreement=agreement,
            confidence=confidence,
            sources=sources,
            blockers=blockers,
            notes=tuple(notes),
        )


market_intelligence = MarketIntelligence()
