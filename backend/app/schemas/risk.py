from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RiskPolicyPayload(BaseModel):
    """Every limit is optional on update; omitted fields keep their value."""

    max_daily_loss_percent: Decimal | None = Field(default=None, ge=0, le=100)
    max_total_loss_percent: Decimal | None = Field(default=None, ge=0, le=100)
    max_risk_per_trade_percent: Decimal | None = Field(default=None, ge=0, le=100)
    max_open_positions: int | None = Field(default=None, ge=0, le=500)
    max_total_exposure_ratio: Decimal | None = Field(default=None, ge=0, le=1000)
    max_symbol_exposure_percent: Decimal | None = Field(default=None, ge=0, le=100)
    max_correlated_positions: int | None = Field(default=None, ge=0, le=500)
    warn_at_percent: Decimal | None = Field(default=None, ge=1, le=100)


class RiskPolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: str
    max_daily_loss_percent: Decimal
    max_total_loss_percent: Decimal
    max_risk_per_trade_percent: Decimal
    max_open_positions: int
    max_total_exposure_ratio: Decimal
    max_symbol_exposure_percent: Decimal
    max_correlated_positions: int
    warn_at_percent: Decimal
    day_start_equity: Decimal | None
    day_started_at: datetime | None
    peak_equity: Decimal | None
    updated_at: datetime | None


class PositionPayload(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    side: str = Field(default="BUY", max_length=8)
    volume: Decimal = Field(ge=0)
    entry_price: Decimal = Field(ge=0)
    current_price: Decimal | None = Field(default=None, ge=0)
    pnl: Decimal = Decimal("0")


class TradePayload(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    side: str = Field(default="BUY", max_length=8)
    volume: Decimal = Field(gt=0)
    entry_price: Decimal = Field(gt=0)
    stop_loss: Decimal | None = Field(default=None, ge=0)


class AssessRequest(BaseModel):
    """
    What to assess.

    Equity defaults to the account's recorded equity. Positions are supplied
    by the caller: the engine's position book is not partitioned per account
    in this build, so reading it here would mix other people's trades into
    your risk picture.
    """

    equity: Decimal | None = Field(default=None, ge=0)
    positions: list[PositionPayload] = Field(default_factory=list)
    trade: TradePayload | None = None


class RuleResultResponse(BaseModel):
    rule: str
    status: str
    used: Decimal
    limit: Decimal
    unit: str
    headroom: Decimal
    utilisation_percent: Decimal
    detail: str


class RiskAssessmentResponse(BaseModel):
    account_id: str
    decision: str
    allowed: bool
    reasons: list[str]
    equity: Decimal
    day_start_equity: Decimal
    peak_equity: Decimal
    exposure: Decimal
    open_positions: int
    rules: list[RuleResultResponse]
