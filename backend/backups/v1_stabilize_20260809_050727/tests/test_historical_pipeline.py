from app.market_data.historical.loaders.csv_loader import CSVMarketLoader
from app.market_data.historical.loaders.historical_service import HistoricalDataService

loader = CSVMarketLoader()
service = HistoricalDataService(loader)

result = service.load_and_validate(
    "tests/data/XAUUSD_H1.csv"
)

print("HISTORICAL RESULT:", result)
