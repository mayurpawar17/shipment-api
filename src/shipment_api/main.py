from typing import Any

from fastapi import FastAPI, HTTPException, status
from .datbase import shipment_data
from .schemas import Shipment, ShipmentResponse,ShipmentCreate, ShipmentUpdate
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Shipment API is running!"}



@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments()->list[ShipmentResponse]:
    '''get all shipments'''
    return [ShipmentResponse(**shipment.dict()) for shipment in shipment_data]

@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int) -> ShipmentResponse:
    '''get a specific shipment by ID'''
    for shipment in shipment_data:
        if shipment.shipment_id == shipment_id:
            return ShipmentResponse(**shipment.dict())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")


@app.post("/shipments", response_model=ShipmentResponse)
def create_shipment(shipment: ShipmentCreate)->ShipmentResponse:
    '''create a new shipment'''
    new_shipment_id = max([s.shipment_id for s in shipment_data], default=0) + 1
    shipment = Shipment(shipment_id=new_shipment_id,status="Created", **shipment.dict())
    shipment_data.append(shipment)
    return ShipmentResponse(**shipment.dict())

@app.put("/shipments/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(shipment_id: int, updated_shipment: ShipmentUpdate) -> ShipmentResponse:
    '''update an existing shipment by ID'''
    for index, shipment in enumerate(shipment_data):
        if shipment.shipment_id == shipment_id:
            shipment_data[index] = shipment.model_copy(
                update=updated_shipment.model_dump(exclude_unset=True)
            )
            return ShipmentResponse(**shipment_data[index].model_dump())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")


@app.delete("/shipments/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int) -> None:
    '''delete a shipment by ID'''
    for index, shipment in enumerate(shipment_data):
        if shipment.shipment_id == shipment_id:
            del shipment_data[index]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

@app.get("/scalar",include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
