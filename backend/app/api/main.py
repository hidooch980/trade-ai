import asyncio
from fastapi import FastAPI
from app.api.routes import websocket_market
from app.api.routes import market_status
from app.api.routes import dashboard
from app.api.routes import backtest
from app.api.routes import live_market
from app.api.routes import market_signal
from app.api.routes import trading
from app.api.routes.signal import router as signal_router
from app.market.stream.market_stream_worker import market_stream_worker

app=FastAPI(title="Trade-AI API",version="1.0.0")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(
        market_stream_worker.start("XAUUSD")
    )


app.include_router(dashboard.router)
app.include_router(backtest.router)
app.include_router(live_market.router)
app.include_router(market_signal.router)
app.include_router(signal_router)
app.include_router(websocket_market.router)
app.include_router(market_status.router)
app.include_router(trading.router)

@app.get("/")
def root():
    return {"status":"RUNNING","system":"Trade-AI Enterprise"}

@app.get("/health")
def health():
    return {"status":"HEALTHY"}
