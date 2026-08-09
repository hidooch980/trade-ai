from fastapi import APIRouter
from app.market_data.store.market_store import market_store

router = APIRouter()

@router.get("/market/status")
def market_status():
    return {
        "status": "RUNNING",
        "symbol": "XAUUSD",
        "engine": "LIVE_MARKET",
        "stream": "ACTIVE"
    }
