from typing import Any

from fastapi import FastAPI, HTTPException, status
from .datbase import shipment_data
from .schemas import Shipment, ShipmentResponse,ShipmentCreate
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Shipment API is running!"}


@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments()->list[ShipmentResponse]:
    return [ShipmentResponse(**shipment.dict()) for shipment in shipment_data]

@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int) -> ShipmentResponse:
    for shipment in shipment_data:
        if shipment.shipment_id == shipment_id:
            return ShipmentResponse(**shipment.dict())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")


@app.post("/shipments", response_model=ShipmentResponse)
def create_shipment(shipment: ShipmentCreate)->ShipmentResponse:
    shipment_data.append(shipment)
    return ShipmentResponse(**shipment.dict())

@app.get("/scalar",include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
