from app.market_data.models.candle import Candle
from app.market_data.models.tick import Tick

class DataValidator:

    def validate_candle(self, candle: Candle):
        errors = []

        if candle.open <= 0 or candle.high <= 0 or candle.low <= 0 or candle.close <= 0:
            errors.append("invalid_price")

        if candle.high < candle.low:
            errors.append("invalid_high_low")

        if candle.close > candle.high or candle.close < candle.low:
            errors.append("close_out_of_range")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def validate_tick(self, tick: Tick):
        errors = []

        if tick.bid <= 0 or tick.ask <= 0:
            errors.append("invalid_price")

        if tick.ask < tick.bid:
            errors.append("invalid_spread")

        if tick.spread < 0:
            errors.append("negative_spread")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
