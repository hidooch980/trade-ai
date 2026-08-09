from fastapi import APIRouter, Depends

from app.execution.position_store import position_store
from app.execution.trade_history import trade_history
from app.execution.close_manager import close_manager
from app.execution.position_monitor import position_monitor
from app.market.market_monitor import market_monitor
from app.execution.order_flow import order_flow
from app.ai.journal.trade_journal import trade_journal
from app.market.bridge.mt5_bridge import mt5_bridge
from app.security.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/api/trading",
    dependencies=[Depends(get_current_user)],
)


@router.get("/positions")
async def positions():
    return {
        "positions": position_store.get_all()
    }


@router.get("/history")
async def history():
    return {
        "trades": trade_history.closed_trades
    }


@router.post("/close/{ticket}")
async def close_position(ticket: str):
    result = await close_manager.close(
        mt5_bridge,
        ticket,
        reason="MANUAL_CLOSE"
    )

    return result


@router.post("/monitor")
async def monitor(data: dict):
    return {
        "positions": position_monitor.update(data)
    }


@router.post("/tick")
async def tick(data: dict):
    positions = market_monitor.update_price(data)

    return {
        "prices": data,
        "positions": positions
    }


@router.post("/execute")
async def execute_order(data: dict):
    return await order_flow.process(
        data["symbol"],
        data["signal"],
        data["risk"]
    )


@router.get("/journal")
async def journal():
    return {
        "journal": trade_journal.all()
    }
