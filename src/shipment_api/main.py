from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from .database import Base, engine
from .models import User  # noqa: F401 - imported before table creation
from .routers.users import router as users_router


# FastAPI creates the HTTP application and generates its OpenAPI documentation.
app = FastAPI(title="FastAPI with SQLAlchemy + Pydantic + Postgresql")

# Importing the models before this call registers their tables with Base.metadata.
# Alembic migrations should be used instead of create_all for production schemas.
Base.metadata.create_all(bind=engine)

# User endpoints are kept in their own router so this entry point stays small.
app.include_router(users_router)


@app.get("/")
async def root():
    # A lightweight health-style endpoint confirms that the API is reachable.
    return {"message": "Shipment API is running!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar():
    # Scalar renders interactive API documentation from FastAPI's OpenAPI schema.
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
