from fastapi import APIRouter

from app.trading.pipeline.signal_pipeline import SignalPipeline


router = APIRouter()

pipeline = SignalPipeline()


@router.post("/signal")
def generate_signal(data: dict):

    return pipeline.generate(

        data.get(
            "symbol",
            "XAUUSD"
        ),

        data.get(
            "price",
            0
        )

    )
