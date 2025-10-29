# main_in_memory.py
# A complete, production-ready FastAPI application with in-memory data storage.

from __future__ import annotations

import datetime
from enum import Enum
from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# --- 1. PYDANTIC MODELS & ENUMS ---

class UserRole(str, Enum):
    """Enumeration for user roles based on the database schema."""
    NEW_HIRE = "new_hire"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"


class UserBase(BaseModel):
    """Base model for user data, containing common fields."""
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The full name of the user.",
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        ...,
        description="The user's unique email address.",
        examples=["john.doe@example.com"]
    )
    sso_identifier: Optional[str] = Field(
        None,
        max_length=100,
        description="Single Sign-On identifier, if applicable.",
        examples=["john.doe.sso"]
    )
    role: UserRole = Field(
        ...,
        description="The role of the user within the system.",
        examples=[UserRole.NEW_HIRE]
    )
    manager_id: Optional[int] = Field(
        None,
        description="The ID of the user's manager. Null if not applicable.",
        examples=[1]
    )
    hire_date: Optional[datetime.date] = Field(
        None,
        description="The date the user was hired.",
        examples=["2024-01-15"]
    )


class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.
    This model is used for the request body of the POST endpoint.
    """
    pass


class UserUpdate(BaseModel):
    """
    Pydantic model for updating an existing user.
    All fields are optional to allow for partial updates.
    """
    full_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="The full name of the user.",
        examples=["Jane Doe"]
    )
    email: Optional[EmailStr] = Field(
        None,
        description="The user's unique email address.",
        examples=["jane.doe@example.com"]
    )
    sso_identifier: Optional[str] = Field(
        None,
        max_length=100,
        description="Single Sign-On identifier, if applicable.",
        examples=["jane.doe.sso"]
    )
    role: Optional[UserRole] = Field(
        None,
        description="The role of the user within the system.",
        examples=[UserRole.MANAGER]
    )
    manager_id: Optional[int] = Field(
        None,
        description="The ID of the user's manager.",
        examples=[2]
    )
    hire_date: Optional[datetime.date] = Field(
        None,
        description="The date the user was hired.",
        examples=["2023-12-01"]
    )


class UserResponse(UserBase):
    """
    Pydantic model for API responses containing user data.
    Includes server-generated fields like user_id and timestamps.
    """
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(
        ...,
        description="The unique identifier for the user.",
        examples=[1]
    )
    created_at: datetime.datetime = Field(
        ...,
        description="The timestamp when the user was created (UTC).",
        examples=["2024-01-01T12:00:00Z"]
    )
    updated_at: datetime.datetime = Field(
        ...,
        description="The timestamp when the user was last updated (UTC).",
        examples=["2024-01-02T15:30:00Z"]
    )


# --- 2. IN-MEMORY DATABASE ---

# A simple list of dictionaries to act as our in-memory database.
# Each dictionary represents a user record.
fake_db: List[Dict] = [
    {
        "user_id": 1,
        "full_name": "Alice Johnson",
        "email": "alice.j@example.com",
        "sso_identifier": "alice.johnson.sso",
        "role": "manager",
        "manager_id": None,
        "hire_date": datetime.date(2022, 1, 15),
        "created_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10),
        "updated_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5),
    },
    {
        "user_id": 2,
        "full_name": "Bob Smith",
        "email": "bob.s@example.com",
        "sso_identifier": "bob.smith.sso",
        "role": "new_hire",
        "manager_id": 1,
        "hire_date": datetime.date(2023, 8, 1),
        "created_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=8),
        "updated_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2),
    },
    {
        "user_id": 3,
        "full_name": "Charlie Brown",
        "email": "charlie.b@example.com",
        "sso_identifier": None,
        "role": "hr_admin",
        "manager_id": None,
        "hire_date": datetime.date(2021, 5, 20),
        "created_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=20),
        "updated_at": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1),
    },
]

# A simple counter to generate unique IDs for new users.
# Initialized to the max ID in the fake data to avoid collisions.
user_id_counter = max(user.get("user_id", 0) for user in fake_db) if fake_db else 0


# --- 3. FASTAPI APPLICATION SETUP ---

app = FastAPI(
    title="Employee Onboarding Tool API",
    description="API for managing employees, onboarding plans, and related resources.",
    version="0.1.0-prototype",
)


# --- 4. API ENDPOINTS ---

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
def create_user(user: UserCreate) -> Dict:
    """
    Create a new user.

    - Accepts a `UserCreate` object in the request body.
    - Checks for email uniqueness.
    - Generates a new unique `user_id`.
    - Adds the user to the in-memory database.
    - Returns the newly created user object with a `201 Created` status.
    """
    # Check for email uniqueness
    if any(db_user["email"] == user.email for db_user in fake_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    global user_id_counter
    user_id_counter += 1
    now = datetime.datetime.now(datetime.timezone.utc)

    new_user = user.model_dump()
    new_user.update({
        "user_id": user_id_counter,
        "created_at": now,
        "updated_at": now,
    })

    fake_db.append(new_user)
    return new_user


@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_users() -> List[Dict]:
    """
    Retrieve a list of all users in the system.
    """
    return fake_db


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int) -> Dict:
    """
    Retrieve a single user by their ID.

    - Accepts `user_id` as a path parameter.
    - Returns the user object if found.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    for user in fake_db:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {user_id} not found"
    )


@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: UserUpdate) -> Dict:
    """
    Update an existing user's details.

    - Accepts `user_id` as a path parameter and a `UserUpdate` object.
    - Performs a partial update: only the fields provided in the request body are modified.
    - Returns the fully updated user object.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    db_user_index = -1
    for i, user in enumerate(fake_db):
        if user["user_id"] == user_id:
            db_user_index = i
            break

    if db_user_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    db_user = fake_db[db_user_index]
    update_data = user_update.model_dump(exclude_unset=True)

    # If email is being updated, check for uniqueness among other users
    if "email" in update_data and update_data["email"] != db_user["email"]:
        if any(u["email"] == update_data["email"] for u in fake_db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists.",
            )

    # Apply the updates
    for key, value in update_data.items():
        db_user[key] = value

    db_user["updated_at"] = datetime.datetime.now(datetime.timezone.utc)
    fake_db[db_user_index] = db_user

    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(user_id: int) -> Dict[str, str]:
    """
    Delete a user from the system.

    - Accepts `user_id` as a path parameter.
    - Removes the user from the in-memory database.
    - Returns a success message.
    - Raises a `404 Not Found` error if the user does not exist.
    """
    user_to_delete = None
    for user in fake_db:
        if user["user_id"] == user_id:
            user_to_delete = user
            break

    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    fake_db.remove(user_to_delete)
    return {"message": f"User with ID {user_id} deleted successfully"}