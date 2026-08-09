from app.market_data.validators.data_validator import DataValidator
from app.market_data.candles.candle_manager import candle_manager

class MarketDataService:

    def __init__(self, provider=None):
        self.validator = DataValidator()
        self.provider = provider

    def process_candle(self, candle):
        """
        Validate and normalize a single candle.

        This is intentionally synchronous because the low-level
        validation path does not require an async provider.
        """
        validation = self.validator.validate_candle(candle)

        if not validation.get("valid"):
            return {
                "valid": False,
                "candle": candle.model_dump(),
                "errors": validation.get("errors", []),
            }

        data = candle.model_dump()

        return {
            "valid": True,
            "candle": data,
        }

    def process_tick(self, tick):
        """
        Validate and normalize a single market tick.
        """
        validation = self.validator.validate_tick(tick)

        if not validation.get("valid"):
            return {
                "valid": False,
                "tick": tick.model_dump(),
                "errors": validation.get("errors", []),
            }

        return {
            "valid": True,
            "tick": tick.model_dump(),
        }

    async def get_market_candles(self, symbol, timeframe, limit=100):
        candles = await self.provider.get_candles(symbol, timeframe, limit)

        result = []

        for candle in candles:
            validation = self.validator.validate_candle(candle)

            if validation["valid"]:
                data = candle.model_dump()
                result.append(data)
                candle_manager.push(
                    symbol,
                    data["open"],
                    data["high"],
                    data["low"],
                    data["close"],
                    data.get("volume",0),
                    timeframe,
                    data.get("timestamp")
                )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "count": len(result),
            "candles": result
        }

    async def get_market_ticks(self, symbol, limit=100):
        ticks = await self.provider.get_ticks(symbol, limit)

        result = []

        for tick in ticks:
            validation = self.validator.validate_tick(tick)

            if validation["valid"]:
                result.append(tick.model_dump())

        return {
            "symbol": symbol,
            "count": len(result),
            "ticks": result
        }
