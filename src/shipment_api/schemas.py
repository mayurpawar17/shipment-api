from pydantic import BaseModel, Field


class BaseShipment(BaseModel):
    shipment_id: int = Field(..., gt=0, description="Unique identifier for the shipment")
    content: str = Field(..., max_length=100, description="Description of the shipment content")
    destination: str = Field(..., max_length=100, description="Destination of the shipment")

class Shipment(BaseShipment):
    status: str = Field(..., max_length=50, description="Current status of the shipment")


class ShipmentResponse(BaseShipment):
    status: str = Field(..., max_length=50, description="Current status of the shipment")

class ShipmentCreate(BaseModel):
    content: str = Field(..., max_length=100, description="Description of the shipment content")
    destination: str = Field(..., max_length=100, description="Destination of the shipment")

class ShipmentUpdate(BaseModel):
    content: str | None = Field(None, max_length=100, description="Description of the shipment content")
    destination: str | None = Field(None, max_length=100, description="Destination of the shipment")
    status: str | None = Field(None, max_length=50, description="Current status of the shipment")