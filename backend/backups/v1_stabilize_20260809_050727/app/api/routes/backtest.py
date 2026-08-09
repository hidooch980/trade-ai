from fastapi import APIRouter
from pydantic import BaseModel

from app.market_data.historical.loaders.csv_loader import CSVMarketLoader
from app.backtest.backtest_engine import backtest_engine


router = APIRouter()


class BacktestRequest(BaseModel):

    symbol: str
    file: str


@router.post("/backtest/run")
async def run_backtest(
    data: BacktestRequest
):

    candles = CSVMarketLoader().load(
        data.file
    )


    result = backtest_engine.run(
        data.symbol,
        [
            c.model_dump()
            for c in candles
        ]
    )


    return result
