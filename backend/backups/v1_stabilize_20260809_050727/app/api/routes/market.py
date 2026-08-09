from fastapi import APIRouter
from app.data.market_storage import market_storage

from app.market_data.live.tick_feed import TickFeed
from app.market_data.candle.candle_builder import CandleBuilder
from app.market_data.store.market_store import market_store
from app.chart_ai.live.smart_money_live import SmartMoneyLive


router = APIRouter()

feed = TickFeed()
candle = CandleBuilder()
history = market_store.history
smart_money = SmartMoneyLive()


@router.post("/market/tick")
def tick(data: dict):
    print("=== MARKET ROUTE ACTIVE ===", data)

    live = feed.update(
        data["symbol"],
        data["price"]
    )

    candle_data = candle.update(
        data["symbol"],
        data["price"]
    )

    timeframe_data = market_store.timeframes.add(candle_data)

    history_data = history.add(
        data["symbol"],
        candle_data
    )

    analysis = smart_money.analyze(
        history.get(data["symbol"])
    )

    market_storage.save(data)
    return {
        "tick": live,
        "candle": candle_data,
        "history": history_data,
        "timeframes": timeframe_data,
        "smart_money": analysis
    }


@router.get("/market/history/{symbol}")
def get_history(symbol: str):

    return {
        "symbol": symbol,
        "candles": history.get(symbol)
    }
