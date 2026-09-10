import logging
from collections.abc import Generator

from dotenv import dotenv_values
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

database_url = dotenv_values(".env").get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    engine = create_engine(database_url)
else:
    engine = create_engine(
        "sqlite:///user.db",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@event.listens_for(engine, "connect")
def log_database_connection(dbapi_connection, connection_record):
    logger.info(
        "Connected to database: %s",
        engine.url.render_as_string(hide_password=True),
    )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
