from decimal import Decimal

from pydantic import BaseModel, Field

from app.market_intelligence import SignalKind


class SignalPayload(BaseModel):
    kind: SignalKind
    #: 0–100, where 50 is no opinion. Out of range is clamped.
    value: Decimal
    #: How much the source trusts its own read, 0–100.
    confidence: Decimal = Decimal("100")
    source: str = Field(default="", max_length=64)
    note: str = Field(default="", max_length=200)


class MarketViewRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    signals: list[SignalPayload] = Field(default_factory=list, max_length=32)
    #: Hard reasons not to trade regardless of the read.
    blockers: list[str] = Field(default_factory=list, max_length=16)


class SourceWeightResponse(BaseModel):
    kind: str
    value: Decimal
    confidence: Decimal
    weight: Decimal
    contribution: Decimal
    source: str
    note: str


class MarketViewResponse(BaseModel):
    symbol: str
    score: Decimal
    bias: str
    decision: str
    actionable: bool
    agreement: Decimal
    confidence: Decimal
    sources: list[SourceWeightResponse]
    blockers: list[str]
    notes: list[str]


class SignalKindInfo(BaseModel):
    kind: str
    default_weight: Decimal


class IntelligenceMetaResponse(BaseModel):
    kinds: list[SignalKindInfo]
    strong_threshold: Decimal
    lean_threshold: Decimal
    min_agreement: Decimal
    min_confidence: Decimal
