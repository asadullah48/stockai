from fastapi.testclient import TestClient
from stockai.server import app

client = TestClient(app)

def test_server_dashboard_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "StockAI" in res.text

def test_server_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_server_readyz():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["supply_chain_agents_active"] == 4

def test_server_process_sku_api():
    payload = {
        "sku": "SKU-TEST-01",
        "item_name": "Test Wireless Mouse",
        "category": "Electronics",
        "current_stock": 8,
        "safety_stock_threshold": 20,
        "daily_run_rate": 4.0,
        "unit_cost_usd": 15.00,
        "lead_time_days": 5,
        "vendor_name": "Test Vendor Corp",
        "vendor_email": "orders@testvendor.com"
    }
    res = client.post("/api/v1/inventory/process-sku", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["purchase_order"]["total_amount_usd"] > 0
    assert data["monitoring"]["is_reorder_required"] is True
