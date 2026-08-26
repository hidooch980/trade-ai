"""
The risk brain.

A pure decision layer: give it what an account looks like right now and, if
you like, a trade you are thinking of placing, and it answers whether that is
allowed, which rule is closest to biting, and how much room is left under
each one.

Nothing here reads a database, a broker or a clock beyond what it is handed,
so every answer is reproducible from its inputs — which is what makes a risk
decision auditable rather than a matter of opinion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import Enum

from app.market.universe.symbol_universe import canonical, category

ZERO = Decimal("0")
HUNDRED = Decimal("100")


def money(value) -> Decimal:
    """
    Decimal or 0.

    NaN and infinity are rejected as well as unparseable input: they survive
    Decimal() but raise on the first comparison, which would turn a bad limit
    into a crash halfway through an assessment.
    """
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return ZERO

    return value if value.is_finite() else ZERO


# Notional units per lot, by asset class. These mirror the divisors already
# used by RiskGovernor.calculate_position_size, so sizing and risk assessment
# agree with each other. They are approximations: real contract sizes are
# broker-specific and a live integration should read them from the terminal.
CONTRACT_UNITS: dict[str, Decimal] = {
    "FOREX": Decimal("100000"),
    "METALS": Decimal("100"),
    "INDICES": Decimal("1"),
    "CRYPTO": Decimal("1"),
}
DEFAULT_UNITS = Decimal("1")


def contract_units(symbol: str) -> Decimal:
    return CONTRACT_UNITS.get(category(canonical(symbol or "")), DEFAULT_UNITS)


class RuleStatus(str, Enum):
    OK = "OK"
    WARN = "WARN"
    BREACH = "BREACH"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


class Rule(str, Enum):
    DAILY_LOSS = "DAILY_LOSS"
    TOTAL_LOSS = "TOTAL_LOSS"
    TRADE_RISK = "TRADE_RISK"
    OPEN_POSITIONS = "OPEN_POSITIONS"
    TOTAL_EXPOSURE = "TOTAL_EXPOSURE"
    SYMBOL_EXPOSURE = "SYMBOL_EXPOSURE"
    CORRELATED_POSITIONS = "CORRELATED_POSITIONS"


@dataclass(frozen=True)
class RiskPolicy:
    """
    The limits an account trades under.

    Percentages are of the reference the rule names: the day's opening equity
    for the daily loss, the equity peak for total loss, current equity for
    per-trade risk.
    """

    max_daily_loss_percent: Decimal = Decimal("5")
    max_total_loss_percent: Decimal = Decimal("10")
    max_risk_per_trade_percent: Decimal = Decimal("1")
    max_open_positions: int = 5
    max_total_exposure_ratio: Decimal = Decimal("10")
    max_symbol_exposure_percent: Decimal = Decimal("50")
    max_correlated_positions: int = 3
    # How close to a limit counts as a warning rather than silence.
    warn_at_percent: Decimal = Decimal("80")

    def normalised(self) -> "RiskPolicy":
        return RiskPolicy(
            max_daily_loss_percent=money(self.max_daily_loss_percent),
            max_total_loss_percent=money(self.max_total_loss_percent),
            max_risk_per_trade_percent=money(self.max_risk_per_trade_percent),
            max_open_positions=int(self.max_open_positions),
            max_total_exposure_ratio=money(self.max_total_exposure_ratio),
            max_symbol_exposure_percent=money(self.max_symbol_exposure_percent),
            max_correlated_positions=int(self.max_correlated_positions),
            warn_at_percent=money(self.warn_at_percent),
        )


@dataclass(frozen=True)
class PositionView:
    symbol: str
    side: str = "BUY"
    volume: Decimal = ZERO
    entry_price: Decimal = ZERO
    current_price: Decimal | None = None
    pnl: Decimal = ZERO

    @property
    def price(self) -> Decimal:
        return money(
            self.current_price if self.current_price is not None else self.entry_price
        )

    @property
    def notional(self) -> Decimal:
        return money(self.volume) * self.price * contract_units(self.symbol)

    @property
    def asset_class(self) -> str:
        return category(canonical(self.symbol or ""))


@dataclass(frozen=True)
class ProposedTrade:
    symbol: str
    side: str
    volume: Decimal
    entry_price: Decimal
    stop_loss: Decimal | None = None

    @property
    def notional(self) -> Decimal:
        return money(self.volume) * money(self.entry_price) * contract_units(self.symbol)

    @property
    def risk_amount(self) -> Decimal:
        """
        What the stop is worth if it is hit.

        No stop means unbounded downside, which the caller has to treat as a
        breach rather than as zero risk — see `assess`.
        """
        if self.stop_loss is None:
            return ZERO

        distance = abs(money(self.entry_price) - money(self.stop_loss))
        return distance * money(self.volume) * contract_units(self.symbol)

    @property
    def asset_class(self) -> str:
        return category(canonical(self.symbol or ""))


@dataclass(frozen=True)
class AccountSnapshot:
    balance: Decimal = ZERO
    equity: Decimal = ZERO
    #: Equity at the day's reset. Falls back to balance when unknown.
    day_start_equity: Decimal | None = None
    #: Highest equity ever recorded. Falls back to balance when unknown.
    peak_equity: Decimal | None = None
    positions: tuple[PositionView, ...] = field(default_factory=tuple)

    @property
    def day_reference(self) -> Decimal:
        return money(
            self.day_start_equity if self.day_start_equity is not None else self.balance
        )

    @property
    def peak_reference(self) -> Decimal:
        candidate = money(
            self.peak_equity if self.peak_equity is not None else self.balance
        )
        # A peak below current equity is stale; today's equity is the peak.
        return max(candidate, money(self.equity))

    @property
    def exposure(self) -> Decimal:
        return sum((p.notional for p in self.positions), ZERO)


@dataclass(frozen=True)
class RuleResult:
    rule: Rule
    status: RuleStatus
    used: Decimal
    limit: Decimal
    unit: str
    detail: str = ""

    @property
    def headroom(self) -> Decimal:
        return max(ZERO, self.limit - self.used)

    @property
    def utilisation_percent(self) -> Decimal:
        if self.limit <= ZERO:
            return HUNDRED if self.used > ZERO else ZERO
        return (self.used / self.limit) * HUNDRED


@dataclass(frozen=True)
class RiskVerdict:
    decision: Decision
    rules: tuple[RuleResult, ...]

    @property
    def allowed(self) -> bool:
        return self.decision is not Decision.BLOCK

    @property
    def breaches(self) -> tuple[RuleResult, ...]:
        return tuple(r for r in self.rules if r.status is RuleStatus.BREACH)

    @property
    def warnings(self) -> tuple[RuleResult, ...]:
        return tuple(r for r in self.rules if r.status is RuleStatus.WARN)

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(r.rule.value for r in self.breaches) or tuple(
            r.rule.value for r in self.warnings
        )


class RiskBrain:
    """Turns a snapshot and a policy into a verdict."""

    def _grade(
        self,
        rule: Rule,
        used: Decimal,
        limit: Decimal,
        unit: str,
        policy: RiskPolicy,
        detail: str = "",
        breach_at_equal: bool = True,
    ) -> RuleResult:
        used = money(used)
        limit = money(limit)

        if limit <= ZERO:
            # A zero limit means the activity is not permitted at all.
            status = RuleStatus.BREACH if used > ZERO else RuleStatus.OK
        elif (used >= limit) if breach_at_equal else (used > limit):
            status = RuleStatus.BREACH
        elif used >= limit * policy.warn_at_percent / HUNDRED:
            status = RuleStatus.WARN
        else:
            status = RuleStatus.OK

        return RuleResult(
            rule=rule, status=status, used=used, limit=limit, unit=unit, detail=detail
        )

    def assess(
        self,
        snapshot: AccountSnapshot,
        policy: RiskPolicy | None = None,
        trade: ProposedTrade | None = None,
    ) -> RiskVerdict:
        policy = (policy or RiskPolicy()).normalised()
        equity = money(snapshot.equity)

        rules: list[RuleResult] = []

        # --- loss against the day's opening equity ------------------------
        day_reference = snapshot.day_reference
        daily_loss = max(ZERO, day_reference - equity)
        daily_loss_percent = (
            (daily_loss / day_reference * HUNDRED) if day_reference > ZERO else ZERO
        )
        rules.append(
            self._grade(
                Rule.DAILY_LOSS,
                daily_loss_percent,
                policy.max_daily_loss_percent,
                "percent",
                policy,
                detail=f"{daily_loss} below the day's opening equity",
            )
        )

        # --- drawdown from the equity peak --------------------------------
        peak = snapshot.peak_reference
        drawdown = max(ZERO, peak - equity)
        drawdown_percent = (drawdown / peak * HUNDRED) if peak > ZERO else ZERO
        rules.append(
            self._grade(
                Rule.TOTAL_LOSS,
                drawdown_percent,
                policy.max_total_loss_percent,
                "percent",
                policy,
                detail=f"{drawdown} below the equity peak",
            )
        )

        # --- the proposed trade -------------------------------------------
        if trade is not None:
            if trade.stop_loss is None:
                # Unbounded downside cannot be measured against a limit, so it
                # is reported as a breach rather than as zero risk.
                rules.append(
                    RuleResult(
                        rule=Rule.TRADE_RISK,
                        status=RuleStatus.BREACH,
                        used=ZERO,
                        limit=policy.max_risk_per_trade_percent,
                        unit="percent",
                        detail="NO_STOP_LOSS",
                    )
                )
            else:
                trade_risk_percent = (
                    (trade.risk_amount / equity * HUNDRED) if equity > ZERO else HUNDRED
                )
                rules.append(
                    self._grade(
                        Rule.TRADE_RISK,
                        trade_risk_percent,
                        policy.max_risk_per_trade_percent,
                        "percent",
                        policy,
                        detail=f"{trade.risk_amount} at risk if the stop is hit",
                        breach_at_equal=False,
                    )
                )

        # --- how many positions would be open -----------------------------
        open_count = Decimal(len(snapshot.positions) + (1 if trade else 0))

        rules.append(
            self._grade(
                Rule.OPEN_POSITIONS,
                open_count,
                Decimal(policy.max_open_positions),
                "positions",
                policy,
                breach_at_equal=False,
            )
        )

        # --- notional exposure against equity -----------------------------
        exposure = snapshot.exposure + (trade.notional if trade else ZERO)
        exposure_ratio = (exposure / equity) if equity > ZERO else ZERO
        rules.append(
            self._grade(
                Rule.TOTAL_EXPOSURE,
                exposure_ratio,
                policy.max_total_exposure_ratio,
                "ratio",
                policy,
                detail=f"{exposure} notional",
                breach_at_equal=False,
            )
        )

        # --- concentration in one symbol ----------------------------------
        by_symbol: dict[str, Decimal] = {}
        for position in snapshot.positions:
            key = canonical(position.symbol or "")
            by_symbol[key] = by_symbol.get(key, ZERO) + position.notional
        if trade:
            key = canonical(trade.symbol or "")
            by_symbol[key] = by_symbol.get(key, ZERO) + trade.notional

        # Concentration only says something once there is a book to be
        # concentrated. With a single position it is trivially 100% and would
        # block every opening trade; absolute size is TOTAL_EXPOSURE's job.
        position_count = len(snapshot.positions) + (1 if trade else 0)

        if position_count >= 2 and exposure > ZERO and by_symbol:
            worst_symbol, worst_notional = max(by_symbol.items(), key=lambda kv: kv[1])
            concentration = worst_notional / exposure * HUNDRED
        else:
            worst_symbol, concentration = "", ZERO

        rules.append(
            self._grade(
                Rule.SYMBOL_EXPOSURE,
                concentration,
                policy.max_symbol_exposure_percent,
                "percent",
                policy,
                detail=worst_symbol or "NOT_APPLICABLE",
                breach_at_equal=False,
            )
        )

        # --- positions moving together ------------------------------------
        by_class: dict[str, int] = {}
        for position in snapshot.positions:
            by_class[position.asset_class] = by_class.get(position.asset_class, 0) + 1
        if trade:
            by_class[trade.asset_class] = by_class.get(trade.asset_class, 0) + 1

        worst_class, correlated = (
            max(by_class.items(), key=lambda kv: kv[1]) if by_class else ("", 0)
        )
        rules.append(
            self._grade(
                Rule.CORRELATED_POSITIONS,
                Decimal(correlated),
                Decimal(policy.max_correlated_positions),
                "positions",
                policy,
                detail=worst_class,
                breach_at_equal=False,
            )
        )

        statuses = {r.status for r in rules}

        if RuleStatus.BREACH in statuses:
            decision = Decision.BLOCK
        elif RuleStatus.WARN in statuses:
            decision = Decision.WARN
        else:
            decision = Decision.ALLOW

        return RiskVerdict(decision=decision, rules=tuple(rules))


risk_brain = RiskBrain()
