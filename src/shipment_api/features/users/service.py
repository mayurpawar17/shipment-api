from sqlalchemy.orm import Session

from . import repository
from .model import User
from .schema import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    return repository.create_user(db, user)


def get_user(db: Session, user_id: int) -> User | None:
    return repository.get_user(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return repository.get_users(db, skip, limit)
