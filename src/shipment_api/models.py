from sqlalchemy import Column, Integer, String

from .database import Base


# This ORM model maps the User Python class to the users database table.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
