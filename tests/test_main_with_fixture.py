import datetime
import uuid

import pytest
from fastapi.testclient import TestClient


def test_create_user_happy_path_isolated(client: TestClient):
    """
    Tests successful user creation using a fixture-managed client and isolated DB.
    """
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "full_name": "Jane Doe",
        "email": unique_email,
        "sso_identifier": f"sso_{uuid.uuid4().hex[:12]}",
        "role": "manager",  # Valid role
        "manager_id": None,
        "hire_date": datetime.date.today().isoformat()
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201, response.text

    data = response.json()

    # Assert shape and types of the response
    assert "user_id" in data
    assert isinstance(data["user_id"], int)
    assert "full_name" in data
    assert isinstance(data["full_name"], str)
    assert "email" in data
    assert isinstance(data["email"], str)
    assert "role" in data
    assert isinstance(data["role"], str)
    assert "hire_date" in data
    assert isinstance(data["hire_date"], str)
    assert "created_at" in data
    assert "updated_at" in data

    # Assert values from the request are reflected in the response
    assert data["full_name"] == user_data["full_name"]
    assert data["email"] == user_data["email"]
    assert data["role"] == user_data["role"]
    assert data["hire_date"] == user_data["hire_date"]


def test_get_users_happy_path_isolated(client: TestClient):
    """
    Tests retrieving a list of users, ensuring test isolation by creating a
    user within the test.
    """
    # Step 1: Create a user to ensure the list is not empty
    unique_email = f"list_test_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "full_name": "List Test User",
        "email": unique_email,
        "role": "hr_admin",
        "hire_date": "2023-11-01"
    }
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    created_user_id = created_user["user_id"]

    # Step 2: Request the list of all users
    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Find the user we just created in the list
    found_user = next((user for user in data if user["user_id"] == created_user_id), None)

    assert found_user is not None
    assert found_user["email"] == unique_email
    assert found_user["full_name"] == "List Test User"
    assert "user_id" in found_user
    assert "role" in found_user
    assert "created_at" in found_user


# Helper factory to reduce duplication in edge tests
def _make_user_payload(role: str = "manager"):
    return {
        "full_name": f"User {uuid.uuid4().hex[:6]}",
        "email": f"edge_{uuid.uuid4().hex[:8]}@example.com",
        "sso_identifier": f"sso_{uuid.uuid4().hex[:10]}",
        "role": role,
        "manager_id": None,
        "hire_date": datetime.date.today().isoformat(),
    }


@pytest.mark.edge
def test_create_user_duplicate_email_rejected_isolated(client: TestClient):
    """Duplicate email should yield 400 with specific detail message using isolated DB."""
    first_payload = _make_user_payload(role="new_hire")

    # First creation succeeds
    r1 = client.post("/users/", json=first_payload)
    assert r1.status_code == 201
    data1 = r1.json()
    assert data1["email"] == first_payload["email"]

    # Second creation with same email should fail
    r2 = client.post("/users/", json=first_payload)
    assert r2.status_code == 400
    body2 = r2.json()
    assert body2.get("detail") == "An account with this email already exists."


@pytest.mark.edge
def test_get_user_not_found_returns_404_isolated(client: TestClient):
    """Requesting a non-existent user ID should return 404 in isolated DB."""
    # Create a baseline user
    payload = _make_user_payload(role="manager")
    r_create = client.post("/users/", json=payload)
    assert r_create.status_code == 201
    created = r_create.json()
    base_id = created["user_id"]

    missing_id = base_id + 99999
    r_get = client.get(f"/users/{missing_id}")
    assert r_get.status_code == 404
    assert r_get.json().get("detail") == f"User with ID {missing_id} not found"