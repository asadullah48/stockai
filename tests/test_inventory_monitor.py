import pytest
from stockai.core.models import SKUInventoryItem, StockStatus
from stockai.core.inventory_monitor import InventoryMonitor

def test_inventory_monitor_reorder_triggered():
    item = SKUInventoryItem(current_stock=10, safety_stock_threshold=20, daily_run_rate=3.0, lead_time_days=5)
    report = InventoryMonitor.inspect_sku(item)
    assert report.is_reorder_required is True
    assert report.status in [StockStatus.REORDER_TRIGGERED, StockStatus.CRITICAL_STOCKOUT]
