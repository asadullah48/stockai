import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from stockai.core.models import SKUInventoryItem, InventoryAutomationPipelineResult
from stockai.orchestration.stockai_engine import StockAIEngine

app = FastAPI(
    title="StockAI Supply Chain Automation Gateway",
    version="1.0.0",
    description="Autonomous Supply Chain & Inventory Automation Multi-Agent Framework"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = StockAIEngine()

# Mount Static UI Files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"service": "StockAI", "status": "active", "docs": "/docs"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy", "service": "StockAI", "version": "1.0.0"}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "supply_chain_agents_active": 4}

@app.post("/api/v1/inventory/process-sku", response_model=InventoryAutomationPipelineResult)
def process_sku(item: SKUInventoryItem):
    return engine.process_sku(item)
