from typing import Any

from fastapi import FastAPI, HTTPException, status
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

@app.post("/shipments")
def create_shipment_with_request_body( data: dict[str, Any]) -> dict[str, Any]:
    '''Create a new shipment with POST Method and Request Body.'''
    new_shipment_id=max(shipments_db.keys()) + 1;
    shipments_db[new_shipment_id] = {"content": data["content"], "status": "pending"}
    return shipments_db[new_shipment_id]

@app.get("/shipments/{shipment_id}")
def get_shipment_by_path_parameter(shipment_id: int) -> dict[str, Any]:
    if shipment_id not in shipments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments_db[shipment_id]

@app.get("/shipments")
def get_shipment_by_query_parameter(shipment_id: int) -> dict[str, Any]:
    if shipment_id not in shipments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipments_db[shipment_id]

@app.post("/shipments")
def create_shipment( content: str) -> dict[str, Any]:
    '''Create a new shipment with POST Method and Query Parameter.'''
    new_shipment_id=max(shipments_db.keys()) + 1;
    shipments_db[new_shipment_id] = {"content": content, "status": "pending"}
    return shipments_db[new_shipment_id]