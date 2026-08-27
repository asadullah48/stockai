import pytest
from stockai.core.models import SKUInventoryItem
from stockai.orchestration.stockai_engine import StockAIEngine

def test_stockai_engine_pipeline():
    engine = StockAIEngine()
    item = SKUInventoryItem()
    res = engine.process_sku(item)
    assert res.monitoring.sku == item.sku
    assert res.purchase_order.order_quantity > 0
    assert res.automation_latency_ms > 0
