# schemas.py
# Pydantic Models for Request/Response Validation
# Description: This file contains Pydantic models used for API request validation
#              and response serialization in the Employee Onboarding Tool.

from __future__ import annotations

import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


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