from fastapi import APIRouter

from app.market_data.live.tick_feed import tick_feed
from app.ai.memory.strategy_memory import strategy_memory
from app.ai.journal.trade_journal import trade_journal
from app.ai.learning.feedback_loop import feedback_loop


router = APIRouter()


@router.get("/dashboard/status")
async def dashboard_status():

    return {

        "market": tick_feed.get_price(),

        "strategy": strategy_memory.get(
            "XAUUSD",
            "M1"
        ),

        "journal_count": len(
            trade_journal.history()
        ),

        "feedback": feedback_loop.analyze(
            "XAUUSD",
            "M1"
        ),

        "system": "ONLINE"
    }
