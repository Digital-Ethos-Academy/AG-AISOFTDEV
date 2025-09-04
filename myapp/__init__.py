from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

Base = declarative_base()
app = FastAPI()


def get_db():
    """Placeholder dependency used for tests."""
    yield None
