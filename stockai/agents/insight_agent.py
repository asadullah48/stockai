from stockai.core.models import SKUInventoryItem, StockMonitoringReport, DemandForecast, ExecutiveInsight, StockStatus
from stockai.core.llm_client import OllamaClient


class InsightAgent:
    """
    InsightAgent: Turns the numeric outputs of MonitorAgent and ForecastAgent into a
    short executive-readable narrative - the "why" behind the reorder decision.

    Tries a local Ollama LLM first for a fluent, context-aware summary. If Ollama is
    not running (no API key needed - it's free and local), the agent falls back to a
    deterministic, rule-based template built from the same numbers, so the field is
    always populated and the API never depends on an optional local model being up.
    """

    def __init__(self, llm_client: OllamaClient = None):
        self.name = "InsightAgent"
        self.version = "1.0.0"
        self.llm_client = llm_client or OllamaClient()

    def generate_insight(
        self,
        item: SKUInventoryItem,
        monitoring: StockMonitoringReport,
        forecast: DemandForecast,
    ) -> ExecutiveInsight:
        prompt = self._build_prompt(item, monitoring, forecast)
        completion = self.llm_client.generate(prompt)

        if completion:
            return ExecutiveInsight(
                sku=item.sku,
                summary=completion,
                source=f"ollama:{self.llm_client.model}",
            )

        return ExecutiveInsight(
            sku=item.sku,
            summary=self._template_summary(item, monitoring, forecast),
            source="template-fallback",
        )

    @staticmethod
    def _build_prompt(item: SKUInventoryItem, monitoring: StockMonitoringReport, forecast: DemandForecast) -> str:
        return (
            "You are a supply chain analyst. In 2-3 concise sentences, explain the "
            "inventory situation below to a non-technical store owner and justify the "
            "recommended action. Do not repeat raw numbers verbatim, interpret them.\n\n"
            f"SKU: {item.sku} ({item.item_name})\n"
            f"Current stock: {item.current_stock} units\n"
            f"Status: {monitoring.status.value}, risk level: {monitoring.risk_level}\n"
            f"Stockout ETA: {monitoring.stockout_eta_days} days\n"
            f"Reorder point: {monitoring.reorder_point_units} units\n"
            f"30-day forecasted demand: {forecast.predicted_demand_units} units "
            f"(seasonal multiplier {forecast.seasonal_growth_multiplier}x)\n"
            f"Recommended reorder quantity: {forecast.recommended_reorder_quantity} units\n"
        )

    @staticmethod
    def _template_summary(item: SKUInventoryItem, monitoring: StockMonitoringReport, forecast: DemandForecast) -> str:
        if monitoring.status == StockStatus.CRITICAL_STOCKOUT:
            urgency = (
                f"{item.item_name} ({item.sku}) is at critical risk of stocking out in "
                f"roughly {monitoring.stockout_eta_days} days at the current sales pace."
            )
        elif monitoring.status == StockStatus.REORDER_TRIGGERED:
            urgency = (
                f"{item.item_name} ({item.sku}) has crossed its reorder point and should "
                f"be replenished soon to avoid a stockout in about {monitoring.stockout_eta_days} days."
            )
        else:
            urgency = f"{item.item_name} ({item.sku}) is currently within a healthy stock buffer."

        return (
            f"{urgency} Demand over the next {forecast.forecast_window_days} days is projected at "
            f"{forecast.predicted_demand_units} units given a {forecast.seasonal_growth_multiplier}x seasonal "
            f"lift, so a reorder of {forecast.recommended_reorder_quantity} units is recommended to "
            f"cover the {item.lead_time_days}-day supplier lead time with buffer intact."
        )
