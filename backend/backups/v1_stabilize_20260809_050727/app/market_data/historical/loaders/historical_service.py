from app.market_data.validators.data_validator import DataValidator

class HistoricalDataService:

    def __init__(self, loader):
        self.loader = loader
        self.validator = DataValidator()

    def load_and_validate(self, path):
        candles = self.loader.load(path)

        valid_candles = []
        rejected = []

        for candle in candles:
            result = self.validator.validate_candle(candle)

            if result["valid"]:
                valid_candles.append(candle)
            else:
                rejected.append({
                    "candle": candle.model_dump(),
                    "errors": result["errors"]
                })

        return {
            "valid_candles": valid_candles,
            "rejected": rejected,
            "total": len(candles),
            "accepted": len(valid_candles)
        }
