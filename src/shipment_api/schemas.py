from pydantic import BaseModel


# This request schema validates the JSON body before database code runs.
class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    # Allows Pydantic to serialize SQLAlchemy model instances as responses.
    model_config = {"from_attributes": True}