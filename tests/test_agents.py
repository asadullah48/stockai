import pytest
from stockai.core.models import SKUInventoryItem
from stockai.agents.monitor_agent import MonitorAgent
from stockai.agents.forecast_agent import ForecastAgent
from stockai.agents.order_agent import OrderAgent

def test_all_stock_agents():
    item = SKUInventoryItem()
    mon = MonitorAgent().monitor_sku(item)
    fc = ForecastAgent().forecast_demand(item)
    po = OrderAgent().draft_purchase_order(item, fc)
    assert mon.sku == item.sku
    assert fc.recommended_reorder_quantity > 0
    assert po.total_amount_usd > 0
    assert "PO-" in po.po_number
    assert item.vendor_email in po.vendor_email
