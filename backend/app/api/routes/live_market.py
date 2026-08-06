from fastapi import APIRouter
from pydantic import BaseModel

from app.market.loop.live_market_runner import live_market_runner


router = APIRouter()


class TickRequest(BaseModel):
    symbol: str
    price: float
    volume: float = 0


@router.post("/market/tick")
async def market_tick(
    data: TickRequest
):

    result = await live_market_runner.run_tick(
        data.symbol,
        data.price,
        data.volume
    )

    return result
