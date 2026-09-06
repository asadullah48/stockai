from stockai.core.models import SKUInventoryItem
from stockai.core.llm_client import OllamaClient
from stockai.agents.monitor_agent import MonitorAgent
from stockai.agents.forecast_agent import ForecastAgent
from stockai.agents.insight_agent import InsightAgent


def test_insight_agent_falls_back_to_template_when_ollama_unavailable(monkeypatch):
    # No local Ollama server is running in CI/test environments, so the client
    # should short-circuit via OLLAMA_DISABLED instead of waiting out the
    # network timeout, and the agent must still return a usable summary.
    monkeypatch.setenv("OLLAMA_DISABLED", "1")

    item = SKUInventoryItem()
    monitoring = MonitorAgent().monitor_sku(item)
    forecast = ForecastAgent().forecast_demand(item)

    insight = InsightAgent().generate_insight(item, monitoring, forecast)

    assert insight.sku == item.sku
    assert insight.source == "template-fallback"
    assert item.item_name in insight.summary
    assert len(insight.summary) > 20


def test_insight_agent_uses_llm_completion_when_available():
    item = SKUInventoryItem()

    class FakeOllamaClient(OllamaClient):
        def generate(self, prompt: str):
            assert item.sku in prompt
            return "Stock is healthy; no action needed right now."

    monitoring = MonitorAgent().monitor_sku(item)
    forecast = ForecastAgent().forecast_demand(item)

    insight = InsightAgent(llm_client=FakeOllamaClient()).generate_insight(item, monitoring, forecast)

    assert insight.summary == "Stock is healthy; no action needed right now."
    assert insight.source.startswith("ollama:")


def test_ollama_client_returns_none_when_disabled(monkeypatch):
    monkeypatch.setenv("OLLAMA_DISABLED", "true")
    client = OllamaClient()
    assert client.generate("hello") is None
