from fastapi import APIRouter

from app.trading.pipeline.signal_pipeline import SignalPipeline


router = APIRouter()

pipeline = SignalPipeline()


@router.post("/signal")
async def generate_signal(data: dict):

    return await pipeline.generate(

        data.get(
            "symbol",
            "XAUUSD"
        ),

        data.get(
            "price",
            0
        )

    )
