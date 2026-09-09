from typing import Any

from fastapi import FastAPI, HTTPException, status
from .datbase import shipment_data,get_connection
from .schemas import Shipment, ShipmentResponse,ShipmentCreate, ShipmentUpdate,UserCreate
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


@app.post("/users")
def create_user(user: UserCreate):
    '''create a new user'''
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) RETURNING id, name, email, age",
        (user.name, user.email, user.age)
    )
    user_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return {"id": user_id, "name": user.name, "email": user.email, "age": user.age}


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
