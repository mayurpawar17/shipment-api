from .schemas import Shipment
import psycopg

#psycopg is a PostgreSQL driver for Python.

connection = psycopg.connect(
    "postgresql://postgres:postgres@localhost:5432/mydb"
)

def get_connection():
    return connection


shipment_data=[
    Shipment(shipment_id=1, content="Electronics", destination="New York", status="In Transit"),
    Shipment(shipment_id=2, content="Clothing", destination="Los Angeles", status="Delivered"),
    Shipment(shipment_id=3, content="Books", destination="Chicago", status="Pending"),
    Shipment(shipment_id=4, content="Furniture", destination="Houston", status="In Transit"),

]