from pydantic import BaseModel

class Shipment(BaseModel):
    shipment_id: str
    content: str
    destination: str
    status: str