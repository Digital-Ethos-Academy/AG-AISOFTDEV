# main.py
# FastAPI Application with SQLAlchemy Database Integration
# Description: Complete FastAPI backend for the Employee Onboarding Tool
#              integrated with a live SQLite database.

from __future__ import annotations

import datetime
from typing import List, Dict

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

# Import database session dependency
from database import get_db

# Import SQLAlchemy models
from models import User

# Import Pydantic schemas
from schemas import UserCreate, UserUpdate, UserResponse


# --- FASTAPI APPLICATION SETUP ---

app = FastAPI(
    title="Employee Onboarding Tool API",
    description="API for managing employees, onboarding plans, and related resources.",
    version="1.0.0",
)


# --- API ENDPOINTS ---

@app.get("/", tags=["Root"])
def read_root() -> Dict[str, str]:
    """Returns a welcome message for the API root."""
    return {"message": "Welcome to the Employee Onboarding Tool API"}


# --- CRUD Endpoints for Users ---

@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Create a new user.

    - Accepts a `UserCreate` object in the request body.
    - Checks for email uniqueness.
    - Adds the user to the database.
    - Returns the newly created user object with a `201 Created` status.
    """
    # Check for email uniqueness
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # Create new user instance
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        sso_identifier=user.sso_identifier,
        role=user.role.value,  # Convert enum to string
        manager_id=user.manager_id,
        hire_date=user.hire_date,
    )

    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_users(db: Session = Depends(get_db)) -> List[User]:
    """
    Retrieve a list of all users in the system.
    """
    users = db.query(User).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """
    Retrieve a single user by their ID.

    - Accepts `user_id` as a path parameter.
    - Returns the user object if found.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
) -> User:
    """
    Update an existing user's details.

    - Accepts `user_id` as a path parameter and a `UserUpdate` object.
    - Performs a partial update: only the fields provided in the request body are modified.
    - Returns the fully updated user object.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    # Find the user
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Get update data (only fields that were set)
    update_data = user_update.model_dump(exclude_unset=True)

    # If email is being updated, check for uniqueness
    if "email" in update_data and update_data["email"] != db_user.email:
        existing_user = db.query(User).filter(User.email == update_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists.",
            )

    # Apply updates
    for key, value in update_data.items():
        # Handle enum conversion for role
        if key == "role" and value is not None:
            setattr(db_user, key, value.value)
        else:
            setattr(db_user, key, value)

    # Manually update the updated_at timestamp
    db_user.updated_at = datetime.datetime.now(datetime.timezone.utc)

    # Commit changes
    db.commit()
    db.refresh(db_user)

    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Delete a user from the system.

    - Accepts `user_id` as a path parameter.
    - Removes the user from the database.
    - Returns a success message.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    # Find the user
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Delete the user
    db.delete(db_user)
    db.commit()

    return {"message": f"User with ID {user_id} deleted successfully"}