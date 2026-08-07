from fastapi import APIRouter
from app.execution.position_store import position_store
from app.execution.trade_history import trade_history

router=APIRouter(prefix="/api/trading")

@router.get("/positions")
async def positions():
    return {"positions":position_store.get_all()}

@router.get("/history")
async def history():
    return {"trades":trade_history.closed_trades}

@router.post("/close/{ticket}")
async def close_position(ticket:str):
    positions=position_store.get_all()
    closed=None
    for p in positions:
        if p.get("ticket")==ticket:
            closed=p
            break
    if not closed:
        return {"closed":False,"reason":"POSITION_NOT_FOUND"}
    position_store.remove(ticket)
    trade={
        "ticket":ticket,
        "order_id":ticket,
        "symbol":closed["symbol"],
        "side":closed["side"],
        "volume":closed["volume"],
        "entry_price":closed["entry_price"],
        "close_price":closed["current_price"],
        "pnl":closed["pnl"],
        "reason":"MANUAL_CLOSE"
    }
    trade_history.closed_trades.append(trade)
    return {"closed":True,"trade":trade}

from app.execution.position_monitor import position_monitor

@router.post("/monitor/{price}")
async def monitor(price:float):
    return {"positions":position_monitor.update(price)}

from app.market.market_monitor import market_monitor

@router.post("/tick/{price}")
async def tick(price:float):
    positions=market_monitor.update_price(price)
    return {
        "price":price,
        "positions":positions
    }

from app.execution.order_flow import order_flow

@router.post("/execute")
async def execute_order(data:dict):
    return await order_flow.process(
        data["symbol"],
        data["signal"],
        data["risk"]
    )

from app.journal.trade_journal import trade_journal

@router.get("/journal")
async def journal():
    return {"journal": trade_journal.all()}
