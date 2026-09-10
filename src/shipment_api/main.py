import logging

from fastapi import FastAPI
from .database import engine, Base
from scalar_fastapi import get_scalar_api_reference
from .routers.users import router as user_router


# Show application INFO logs, including the database connection message.
logging.basicConfig(level=logging.INFO)

# FastAPI creates the HTTP application and generates its OpenAPI documentation.
app = FastAPI(title="FastAPI with SQLAlchemy + Pydantic + Postgresql")


# Create the table when the application starts. For production schema changes,
# migrations (for example, Alembic) should be used instead.
Base.metadata.create_all(bind=engine)

    

app.include_router(user_router)

@app.get("/")
async def root():
    # A lightweight health-style endpoint confirms that the API is reachable.
    return {"message": "Shipment API is running!"}



@app.get("/scalar",include_in_schema=False)
def get_scalar():
    # Scalar renders interactive API documentation from FastAPI's OpenAPI schema.
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
    
