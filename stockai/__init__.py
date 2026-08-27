"""
StockAI: Autonomous Supply Chain & Inventory Automation Multi-Agent Framework
"""

__version__ = "1.0.0"

from stockai.agents.monitor_agent import MonitorAgent
from stockai.agents.forecast_agent import ForecastAgent
from stockai.agents.order_agent import OrderAgent
from stockai.orchestration.stockai_engine import StockAIEngine

__all__ = [
    "MonitorAgent",
    "ForecastAgent",
    "OrderAgent",
    "StockAIEngine"
]
