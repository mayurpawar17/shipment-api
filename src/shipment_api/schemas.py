class Shipment:
    def __init__(self, shipment_id: str, content: str, destination: str, status: str):
        self.shipment_id = shipment_id
        self.content = content
        self.destination = destination
        self.status = status