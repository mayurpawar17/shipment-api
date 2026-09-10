from fastapi import FastAPI, HTTPException, Depends,status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List,Optional,Any
from scalar_fastapi import get_scalar_api_reference


# FastAPI creates the HTTP application and generates its OpenAPI documentation.
app = FastAPI(title="FastAPI with SQLAlchemy + Pydantic + Postgresql")

# SQLite is used for the current local implementation. The thread option allows
# the same SQLite connection to be used by FastAPI's request-handling threads.
engine = create_engine("sqlite:///user.db", connect_args={"check_same_thread": False})
# A new SQLAlchemy session is created for each request and closed afterward.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base keeps the metadata for all SQLAlchemy table models in this module.
Base = declarative_base()


# This ORM model maps the User Python class to the users database table.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Create the table when the application starts. For production schema changes,
# migrations (for example, Alembic) should be used instead.
Base.metadata.create_all(bind=engine)

# This request schema validates the JSON body before database code runs.
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        # Allows Pydantic to serialize SQLAlchemy model instances as responses.
        from_attributes = True

def get_db():
    # FastAPI injects this session into an endpoint and guarantees cleanup
    # through the finally block after the endpoint finishes.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Convert validated request data into an ORM object, persist it, and reload
    # it so generated values such as the primary-key ID are available.
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Reject invalid IDs before querying the database.
    if user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")
    # Return a clear 404 response instead of exposing a missing database row.
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db.query(User).filter(User.id == user_id).first()


@app.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Pagination prevents this endpoint from loading every user at once.
    return db.query(User).offset(skip).limit(limit).all()
    
@app.get("/")
async def root():
    # A lightweight health-style endpoint confirms that the API is reachable.
    return {"message": "Shipment API is running!"}



@app.get("/scalar",include_in_schema=False)
def get_scalar():
    # Scalar renders interactive API documentation from FastAPI's OpenAPI schema.
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
    
