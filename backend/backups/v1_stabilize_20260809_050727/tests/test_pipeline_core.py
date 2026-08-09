import asyncio

from app.trading.pipeline.signal_pipeline import SignalPipeline


async def main():

    pipeline = SignalPipeline()

    result = await pipeline.generate(
        "BTCUSDT",
        115000
    )

    print("\n=== PIPELINE RESULT ===")

    print("Decision:")
    print(
        result.get("decision")
    )

    print("\nSmart Money:")
    print(
        result.get("smart_money")
    )

    print("\nRisk:")
    print(
        result.get("risk")
    )

    print("\nExecution:")
    print(
        result.get("execution")
    )


if __name__ == "__main__":
    asyncio.run(main())
