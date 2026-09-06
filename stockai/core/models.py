from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class StockStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    REORDER_TRIGGERED = "REORDER_TRIGGERED"
    CRITICAL_STOCKOUT = "CRITICAL_STOCKOUT"

class SKUInventoryItem(BaseModel):
    sku: str = "SKU-9920"
    item_name: str = "Wireless Ergonomic Pro Mouse"
    category: str = "Electronics & Peripherals"
    current_stock: int = 14
    safety_stock_threshold: int = 25
    daily_run_rate: float = 4.5 # units / day
    unit_cost_usd: float = 24.50
    lead_time_days: int = 7
    vendor_name: str = "Apex Precision Components Ltd"
    vendor_email: str = "orders@apexprecision.com"

class StockMonitoringReport(BaseModel):
    sku: str
    status: StockStatus
    stockout_eta_days: float
    reorder_point_units: int
    is_reorder_required: bool
    risk_level: str # LOW | MEDIUM | HIGH

class DemandForecast(BaseModel):
    sku: str
    forecast_window_days: int = 30
    predicted_demand_units: int
    seasonal_growth_multiplier: float
    recommended_reorder_quantity: int
    confidence_interval_percent: float

class ExecutiveInsight(BaseModel):
    sku: str
    summary: str
    source: str  # e.g. "ollama:llama3.2" or "template-fallback"
    generated_at: float = Field(default_factory=time.time)

class PurchaseOrderDraft(BaseModel):
    po_number: str
    sku: str
    item_name: str
    order_quantity: int
    unit_price_usd: float
    total_amount_usd: float
    vendor_name: str
    vendor_email: str
    email_subject: str
    email_body_draft: str
    estimated_delivery_days: int

class InventoryAutomationPipelineResult(BaseModel):
    pipeline_id: str
    sku_item: SKUInventoryItem
    monitoring: StockMonitoringReport
    forecast: DemandForecast
    insight: ExecutiveInsight
    purchase_order: PurchaseOrderDraft
    automation_latency_ms: float
    processed_at: float = Field(default_factory=time.time)
