import pytest
import uuid
import datetime
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.edge
def test_create_user_duplicate_email_rejected():
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    user_payload = {
        "full_name": "Duplicate User",
        "email": unique_email,
        "sso_identifier": uuid.uuid4().hex,
        # Use a valid enum role value (e.g., new_hire, manager, hr_admin)
        "role": "new_hire",
        "manager_id": None,
        "hire_date": datetime.date.today().isoformat(),
    }

    # First request: Create the user successfully
    response1 = client.post("/users/", json=user_payload)
    assert response1.status_code == 201
    data1 = response1.json()
    assert isinstance(data1["user_id"], int)
    assert data1["email"] == unique_email
    assert data1["full_name"] == "Duplicate User"
    assert data1["role"] == "new_hire"

    # Second request: Attempt to create the same user again
    response2 = client.post("/users/", json=user_payload)
    assert response2.status_code == 400
    body2 = response2.json()
    assert body2.get("detail") == "An account with this email already exists."


@pytest.mark.edge
def test_get_user_not_found_returns_404():
    # Step 1: Create a valid user to get a real ID
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    user_payload = {
        "full_name": "Existing User",
        "email": unique_email,
        "sso_identifier": uuid.uuid4().hex,
        "role": "manager",
        "hire_date": datetime.date.today().isoformat(),
    }
    create_response = client.post("/users/", json=user_payload)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert isinstance(created_user["user_id"], int)
    assert created_user["email"] == unique_email
    assert created_user["full_name"] == "Existing User"
    assert created_user["role"] == "manager"

    # Step 2: Compute a non-existent ID
    created_user_id = created_user["user_id"]
    missing_id = created_user_id + 99999

    # Step 3: Request the user with the non-existent ID
    get_response = client.get(f"/users/{missing_id}")
    assert get_response.status_code == 404
    assert get_response.json().get("detail") == f"User with ID {missing_id} not found"