from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


# SQLite is used for the current local implementation and stores data in user.db.
# The thread option allows FastAPI request handlers to use the SQLite connection.
engine = create_engine(
    "sqlite:///user.db",
    connect_args={"check_same_thread": False},
)

# A new SQLAlchemy session is created for each request and closed afterward.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base keeps the metadata for all SQLAlchemy table models.
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    # FastAPI injects this session into an endpoint and cleanup runs afterward.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()