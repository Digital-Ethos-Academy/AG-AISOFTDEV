### Users

-   **`POST /users/`**
    -   **Description:** Creates a new user in the system. Requires a JSON body with user details.
    -   **cURL Example:**
        ```bash
        curl -X POST "http://127.0.0.1:8000/users/" \
        -H "Content-Type: application/json" \
        -d '{
          "full_name": "Amelia Achiever",
          "email": "amelia.achiever@example.com",
          "sso_identifier": "aachiever",
          "role": "new_hire",
          "manager_id": 2,
          "hire_date": "2026-01-15"
        }'
        ```

-   **`GET /users/`**
    -   **Description:** Retrieves a list of all users.
    -   **cURL Example:**
        ```bash
        curl -X GET "http://127.0.0.1:8000/users/"
        ```

-   **`GET /users/{user_id}`**
    -   **Description:** Retrieves a single user by their unique ID.
    -   **cURL Example:**
        ```bash
        curl -X GET "http://127.0.0.1:8000/users/1"
        ```

-   **`PUT /users/{user_id}`**
    -   **Description:** Updates an existing user's information. This is a partial update; only include the fields you want to change.
    -   **cURL Example (Partial Update):**
        ```bash
        curl -X PUT "http://127.0.0.1:8000/users/1" \
        -H "Content-Type: application/json" \
        -d '{
          "role": "software_engineer_i",
          "manager_id": 3
        }'
        ```

-   **`DELETE /users/{user_id}`**
    -   **Description:** Deletes a user from the system by their unique ID.
    -   **cURL Example:**
        ```bash
        curl -X DELETE "http://127.0.0.1:8000/users/1"
        ```

## Request/Response Schemas

Pydantic schemas are used to define the data structures for API requests and responses, ensuring data consistency and validation.

-   **`UserCreate`**: The schema used for the `POST /users/` request body. It includes all required fields for creating a new user:
    -   `full_name` (str)
    -   `email` (str)
    -   `sso_identifier` (str, optional)
    -   `role` (enum: e.g., 'new_hire', 'manager', 'admin')
    -   `manager_id` (int, optional)
    -   `hire_date` (date)

-   **`UserUpdate`**: The schema for the `PUT /users/{user_id}` request body. All fields are optional, allowing for partial updates. It contains a subset of the fields from `UserCreate`.

-   **`UserResponse`**: The schema for the response body when a user object is returned. It includes all user attributes stored in the database, including system-generated fields:
    -   `user_id` (int)
    -   `full_name`, `email`, `sso_identifier`, `role`, `manager_id`, `hire_date`
    -   `created_at` (datetime)
    -   `updated_at` (datetime)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/employee-onboarding-tool.git
    cd employee-onboarding-tool
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI application locally for development, use Uvicorn. The `--reload` flag will automatically restart the server when code changes are detected.