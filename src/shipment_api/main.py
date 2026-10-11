from typing import Any

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Shipment API",
    description="API for managing shipments.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

shipments_db = {
    12345: {"content": "Books", "status": "delivered"},
    67890: {"content": "Electronics", "status": "in_transit"},
}   


@app.get("/health", include_in_schema=False)
def health_check():
    return {"status": "healthy"}


@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")

@app.get("/shipments/latest")
def get_latest_shipment() -> dict[str, Any]:
    id=max(shipments_db.keys());
    return shipments_db[id]

@app.get("/shipments/{shipment_id}")
def get_shipments(shipment_id: int) -> dict[str, Any]:
    return shipments_db.get(shipment_id, {"error": "Shipment not found"})

