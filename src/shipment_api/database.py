import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


# Set DATABASE_URL to the supplied Neon connection string before starting API.
# It is read from the environment so the database password is not committed.
database_url = os.getenv("DATABASE_URL")

if database_url:
    # SQLAlchemy needs +psycopg to select the installed Psycopg 3 driver.
    # This accepts the standard postgresql:// URL supplied by Neon.
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    engine = create_engine(database_url)
else:
    # SQLite fallback for local development when DATABASE_URL is not configured.
    # The thread option allows FastAPI handlers to share SQLite connections.
    engine = create_engine(
        "sqlite:///user.db",
        connect_args={"check_same_thread": False},
    )

# Original SQLite configuration, preserved for reference:
# engine = create_engine("sqlite:///user.db", connect_args={"check_same_thread": False})

# The psycopg[binary] dependency provides the Psycopg 3 PostgreSQL driver.
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
