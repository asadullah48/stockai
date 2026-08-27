from stockai.core.models import SKUInventoryItem, StockMonitoringReport
from stockai.core.inventory_monitor import InventoryMonitor

class MonitorAgent:
    """
    MonitorAgent: Monitors real-time SKU inventory levels and computes stockout velocity.
    """
    def __init__(self):
        self.name = "MonitorAgent"
        self.version = "1.0.0"

    def monitor_sku(self, item: SKUInventoryItem) -> StockMonitoringReport:
        return InventoryMonitor.inspect_sku(item)
