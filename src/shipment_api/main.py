from typing import Any

from fastapi import FastAPI, HTTPException, status
from .datbase import shipment_data
from .schemas import Shipment
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Shipment API is running!"}


@app.get("/shipments")
def get_shipments():
    return shipment_data

@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id:str) ->dict[str,Any]:
    for shipment in shipment_data:
        if shipment.shipment_id == shipment_id:
            return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")


@app.post("/shipments")
def create_shipment(shipment: Shipment)->dict[str,Any]:
    shipment_data.append(shipment)
    return shipment.model_dump()

@app.get("/scalar",include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
