import pytest
from stockai.core.models import SKUInventoryItem
from stockai.core.demand_forecaster import DemandForecaster

def test_demand_forecaster():
    item = SKUInventoryItem(daily_run_rate=5.0, current_stock=20)
    fc = DemandForecaster.forecast(item, window_days=30)
    assert fc.predicted_demand_units > 150
    assert fc.recommended_reorder_quantity >= 50
