from fastapi import APIRouter
from app.market.loop.signal_runner import runner

router = APIRouter()

@router.post("/market/run")
async def run_market_signal():

    result = await runner.run_once()

    return result
