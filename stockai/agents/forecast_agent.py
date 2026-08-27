from stockai.core.models import SKUInventoryItem, DemandForecast
from stockai.core.demand_forecaster import DemandForecaster

class ForecastAgent:
    """
    ForecastAgent: Estimates seasonal demand curve and optimal reorder batch size.
    """
    def __init__(self):
        self.name = "ForecastAgent"
        self.version = "1.0.0"

    def forecast_demand(self, item: SKUInventoryItem) -> DemandForecast:
        return DemandForecaster.forecast(item)
