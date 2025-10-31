"""Database initialization utility.

Creates the SQLite database file and tables if missing, and optionally seeds initial data.

Run manually:
    python -m app.init_db

In container build/runtime you can invoke this script once before serving.
"""
from __future__ import annotations
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from .database import SQLALCHEMY_DATABASE_URL

SEED_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com")


def init_db(seed: bool = True) -> None:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    # Ensure parent directory exists
    db_dir = os.path.join(os.getcwd(), "database")
    os.makedirs(db_dir, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    if seed:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with SessionLocal() as session:
            # Seed an admin user if none exists
            if not session.query(User).first():
                user = User(
                    full_name="System Admin",
                    email=SEED_EMAIL,
                    sso_identifier="admin-sso",
                    role="hr_admin",
                    manager_id=None,
                    hire_date=None,
                )
                session.add(user)
                session.commit()

if __name__ == "__main__":
    init_db(seed=True)
    print("Database initialized.")
