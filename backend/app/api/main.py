import asyncio
from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.i18n.dependencies import get_request_language
from guardian_status_api import router as guardian_router
from app.api.routes import websocket_market
from app.api.routes import market_status
from app.api.routes import dashboard
from app.api.routes import backtest
from app.api.routes import live_market
from app.api.routes import market_signal
from app.api.routes import trading
from app.api.routes import auth
from app.api.routes import admin_users
from app.api.routes.signal import router as signal_router
from app.market.stream.market_stream_worker import market_stream_worker
from app.i18n.routes import router as i18n_router
from app.i18n.errors import http_exception_handler, general_exception_handler

app=FastAPI(title="Trade-AI API",version="1.0.0",dependencies=[Depends(get_request_language)])
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)



@app.on_event("startup")
async def startup_event():
    for symbol in ["EURUSD","GBPUSD","XAUUSD","BTCUSD"]:
        asyncio.create_task(
            market_stream_worker.start(symbol)
        )


app.include_router(dashboard.router)
app.include_router(backtest.router)
app.include_router(live_market.router)
app.include_router(market_signal.router)
app.include_router(signal_router)
app.include_router(websocket_market.router)
app.include_router(market_status.router)
app.include_router(trading.router)
app.include_router(auth.router)
app.include_router(admin_users.router)

@app.get("/")
def root():
    return {"status":"RUNNING","system":"Trade-AI Enterprise"}

@app.get("/health")
def health():
    return {"status":"HEALTHY"}
app.include_router(i18n_router)
app.include_router(guardian_router)
