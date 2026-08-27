from stockai.core.models import SKUInventoryItem, StockMonitoringReport, StockStatus

class InventoryMonitor:
    """
    InventoryMonitor: Evaluates buffer thresholds and calculates reorder point (ROP = d * L + SS).
    """
    @staticmethod
    def inspect_sku(item: SKUInventoryItem) -> StockMonitoringReport:
        reorder_point = int(item.daily_run_rate * item.lead_time_days + item.safety_stock_threshold)
        eta_days = max(0.1, round(item.current_stock / max(0.1, item.daily_run_rate), 1))
        
        if item.current_stock <= (item.safety_stock_threshold / 2):
            status = StockStatus.CRITICAL_STOCKOUT
            risk = "HIGH"
            req = True
        elif item.current_stock <= reorder_point:
            status = StockStatus.REORDER_TRIGGERED
            risk = "MEDIUM"
            req = True
        else:
            status = StockStatus.OPTIMAL
            risk = "LOW"
            req = False

        return StockMonitoringReport(
            sku=item.sku,
            status=status,
            stockout_eta_days=eta_days,
            reorder_point_units=reorder_point,
            is_reorder_required=req,
            risk_level=risk
        )
