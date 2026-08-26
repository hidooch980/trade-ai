"""
Market intelligence over HTTP.

Post the reads you have on an instrument and get back one graded view: the
fused score, which way it leans, how much the sources agree, and which of
them drove the answer.

The endpoint computes; it does not collect. Signals come from the caller
because nothing in this build produces sentiment, macro or flow reads yet —
inventing them here would dress up a guess as a measurement.
"""

from fastapi import APIRouter, Depends

from app.market_intelligence import Signal, market_intelligence
from app.market_intelligence.core import DEFAULT_WEIGHTS, MarketIntelligence
from app.schemas.intelligence import (
    IntelligenceMetaResponse,
    MarketViewRequest,
    MarketViewResponse,
    SignalKindInfo,
    SourceWeightResponse,
)
from app.security.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/intelligence", tags=["intelligence"])


@router.get("/meta", response_model=IntelligenceMetaResponse)
async def meta(_user=Depends(get_current_user)):
    """The signal kinds, their weights, and the thresholds in use."""
    return IntelligenceMetaResponse(
        kinds=[
            SignalKindInfo(kind=kind.value, default_weight=w)
            for kind, w in DEFAULT_WEIGHTS.items()
        ],
        strong_threshold=MarketIntelligence.STRONG,
        lean_threshold=MarketIntelligence.LEAN,
        min_agreement=MarketIntelligence.MIN_AGREEMENT,
        min_confidence=MarketIntelligence.MIN_CONFIDENCE,
    )


@router.post("/view", response_model=MarketViewResponse)
async def market_view(
    data: MarketViewRequest,
    _user=Depends(get_current_user),
):
    result = market_intelligence.assess(
        data.symbol.strip().upper(),
        [
            Signal(
                kind=s.kind,
                value=s.value,
                confidence=s.confidence,
                source=s.source,
                note=s.note,
            )
            for s in data.signals
        ],
        data.blockers,
    )

    return MarketViewResponse(
        symbol=result.symbol,
        score=result.score,
        bias=result.bias.value,
        decision=result.decision.value,
        actionable=result.actionable,
        agreement=result.agreement,
        confidence=result.confidence,
        sources=[
            SourceWeightResponse(
                kind=s.kind.value,
                value=s.value,
                confidence=s.confidence,
                weight=s.weight,
                contribution=s.contribution,
                source=s.source,
                note=s.note,
            )
            for s in result.sources
        ],
        blockers=list(result.blockers),
        notes=list(result.notes),
    )
