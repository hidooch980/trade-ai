from fastapi import APIRouter
import json
from pathlib import Path
from app.analytics.ai_performance_service import ai_performance_service

router = APIRouter(prefix="/api/ai")


@router.get("/performance/{symbol}/{timeframe}")
async def performance(symbol: str, timeframe: str):

    return ai_performance_service.report(
        symbol,
        timeframe
    )


@router.get("/performance")
def ai_performance():

    file = Path("app/learning/data/reward_memory.json")

    if not file.exists():
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "accuracy": 0
        }

    data = json.loads(file.read_text())

    wins = len([
        x for x in data
        if x.get("reward",0) > 0
    ])

    losses = len([
        x for x in data
        if x.get("reward",0) < 0
    ])

    total = wins + losses

    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "accuracy": round((wins / total) * 100, 2) if total else 0
    }
