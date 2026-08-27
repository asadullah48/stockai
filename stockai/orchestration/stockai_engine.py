import time
from stockai.core.models import SKUInventoryItem, InventoryAutomationPipelineResult
from stockai.agents.monitor_agent import MonitorAgent
from stockai.agents.forecast_agent import ForecastAgent
from stockai.agents.order_agent import OrderAgent

class StockAIEngine:
    """
    StockAIEngine: Orchestrates the supply chain lifecycle (Monitor -> Forecast -> Order Draft).
    """
    def __init__(self):
        self.monitor = MonitorAgent()
        self.forecaster = ForecastAgent()
        self.orderer = OrderAgent()

    def process_sku(self, item: SKUInventoryItem) -> InventoryAutomationPipelineResult:
        t0 = time.time()

        monitoring = self.monitor.monitor_sku(item)
        forecast = self.forecaster.forecast_demand(item)
        po = self.orderer.draft_purchase_order(item, forecast)

        latency = (time.time() - t0) * 1000.0

        return InventoryAutomationPipelineResult(
            pipeline_id=f"STK-PIPE-{abs(hash(item.sku)) % 10000}",
            sku_item=item,
            monitoring=monitoring,
            forecast=forecast,
            purchase_order=po,
            automation_latency_ms=max(10.0, latency)
        )
