import logging
from collections.abc import Generator

from dotenv import dotenv_values
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


logger = logging.getLogger(__name__)


# Load the database URL from the local .env file.
database_url = dotenv_values(".env").get("DATABASE_URL")
# Previous environment-variable approach, preserved for reference:
# database_url = os.getenv("DATABASE_URL")

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


@event.listens_for(engine, "connect")
def log_database_connection(dbapi_connection, connection_record):
    # This event runs when SQLAlchemy opens a real DB connection. Passwords are
    # hidden so the connection log is safe to keep in application logs.
    logger.info(
        "Connected to database: %s",
        engine.url.render_as_string(hide_password=True),
    )


def get_db() -> Generator[Session, None, None]:
    # FastAPI injects this session into an endpoint and cleanup runs afterward.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
