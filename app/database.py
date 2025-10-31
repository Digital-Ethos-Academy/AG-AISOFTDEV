# database.py
# Database Session Management for the Employee Onboarding Tool
# Description: This file contains the setup for the database connection,
#              engine, session factory, and the FastAPI dependency for
#              obtaining a database session.

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# The database URL for the SQLite database file.
# Use a path relative to the container WORKDIR (/app) so SQLite file resides in /app/database.
# This allows us to mount a volume at /app/database for persistence.
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/onboarding.db"

# Create the SQLAlchemy engine.
# The `connect_args` is a SQLite-specific configuration.
# `check_same_thread=False` is required because SQLite by default only allows
# one thread to communicate with it, assuming that each thread would open a
# separate connection. FastAPI, being asynchronous, can have multiple threads
# interact with the database for a single request, so this check needs to be disabled.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class, which will be our session factory.
# Each instance of SessionLocal will be a database session.
# `autocommit=False` and `autoflush=False` are standard settings for using
# SQLAlchemy sessions with web frameworks like FastAPI. This gives us explicit
# control over when to commit transactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get a database session.

    This is a generator function that creates a new SQLAlchemy Session for each
    request, yields it to the path operation function, and then ensures it's
    closed after the request is finished, even if an error occurs.

    Yields:
        Generator[Session, None, None]: A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()