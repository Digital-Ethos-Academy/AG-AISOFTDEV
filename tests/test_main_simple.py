import datetime
import uuid

# client fixture provided by conftest.py (TestClient with in-memory DB override)


def test_create_user_happy_path(client):
    """
    Tests the successful creation of a new user via the POST /users/ endpoint.
    """
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "full_name": "Jane Doe",
        "email": unique_email,
        "sso_identifier": f"sso_{uuid.uuid4().hex[:12]}",
        "role": "new_hire",  # valid enum value
        "manager_id": None,
        "hire_date": datetime.date.today().isoformat()
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

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
    assert data["role"] in ["new_hire", "manager", "hr_admin"]  # Enum-defined roles
    assert data["hire_date"] == user_data["hire_date"]


def test_get_users_happy_path(client):
    """
    Tests retrieving a list of all users via the GET /users/ endpoint.
    Ensures the test is independent by creating a user first.
    """
    # Step 1: Create a user to ensure the list is not empty
    unique_email = f"list_test_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "full_name": "List Test User",
        "email": unique_email,
        "role": "manager",
        "hire_date": datetime.date.today().isoformat()
    }
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    created_user_id = create_response.json()["user_id"]

    # Step 2: Make the request to get all users
    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Find the user we just created in the list
    found_user = None
    for user in data:
        if user["user_id"] == created_user_id:
            found_user = user
            break

    assert found_user is not None
    assert found_user["email"] == unique_email
    assert found_user["full_name"] == "List Test User"
    assert "user_id" in found_user
    assert isinstance(found_user["user_id"], int)