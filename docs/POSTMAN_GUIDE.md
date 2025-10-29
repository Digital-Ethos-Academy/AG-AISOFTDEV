# Employee Onboarding Tool API - Postman Guide

This guide explains how to import and use the Postman collection for testing the Employee Onboarding Tool API.

## Files Included

1. **Onboarding_API_Collection.postman_collection.json** - Complete API collection with all endpoints
2. **Onboarding_API_Environment.postman_environment.json** - Environment variables for local development

## Import Instructions

### Step 1: Import the Collection

1. Open Postman
2. Click **Import** button (top left)
3. Select **File** or drag and drop the collection JSON file
4. Choose: `Onboarding_API_Collection.postman_collection.json`
5. Click **Import**

### Step 2: Import the Environment

1. Click **Import** button again
2. Select the environment JSON file
3. Choose: `Onboarding_API_Environment.postman_environment.json`
4. Click **Import**

### Step 3: Activate the Environment

1. Click the environment dropdown (top right)
2. Select **"Onboarding API - Local"**
3. Verify the `base_url` is set to `http://localhost:8000`

## Collection Structure

The collection is organized into three main folders:

### 1. Health Check
- **Get API Root** - Basic connectivity test
- **Get API Docs** - Opens Swagger UI in browser

### 2. Users - CRUD Operations
Complete set of user management endpoints with automated tests:

- **Get All Users** - List all users
- **Get User by ID** - Retrieve single user
- **Get Non-Existent User (404)** - Error handling test
- **Create New User** - Add new user (saves ID to environment)
- **Create User with Duplicate Email (400)** - Validation test
- **Update User (Partial)** - Partial update example
- **Update User Role** - Role change example
- **Delete User** - Remove user
- **Delete Non-Existent User (404)** - Error handling test

### 3. Demo Workflow
A complete onboarding workflow demonstrating the full lifecycle:

1. List All Users
2. Create New Hire
3. View New User Details
4. Complete Onboarding (Update Role)
5. Clean Up (Delete Demo User)

## Running Tests

### Run Individual Requests
1. Select any request from the collection
2. Click **Send**
3. View response in the lower panel
4. Check the **Test Results** tab for automated test results

### Run Entire Collection
1. Click the **...** menu next to the collection name
2. Select **Run collection**
3. Configure run settings (optional)
4. Click **Run Onboarding Tool API**
5. View the test results summary

### Run a Folder
1. Hover over a folder (e.g., "Users - CRUD Operations")
2. Click the **...** menu
3. Select **Run folder**

## Automated Tests

Each request includes automated tests that verify:
- HTTP status codes
- Response structure
- Data validation
- Error handling

Tests will appear in the **Test Results** tab after running a request.

## Environment Variables

The collection uses these variables (managed automatically):

- `base_url` - API base URL (default: http://localhost:8000)
- `created_user_id` - Saved after creating a user
- `demo_user_id` - Saved during demo workflow

These variables are used in URLs like: `{{base_url}}/users/{{created_user_id}}`

## Request Examples

### Create User Request Body
```json
{
  "full_name": "Jane Smith",
  "email": "jane.smith@momentum.com",
  "sso_identifier": "auth0|jane.smith",
  "role": "new_hire",
  "manager_id": 2,
  "hire_date": "2025-11-15"
}
```

### Update User Request Body (Partial)
```json
{
  "full_name": "Updated Name"
}
```

### Valid Roles
- `new_hire`
- `manager`
- `hr_admin`

## Tips for Demonstration

1. **Start with Health Check** - Verify API is running
2. **Run Demo Workflow** - Shows complete user lifecycle
3. **Show Error Handling** - Run the 404 and 400 test cases
4. **View Test Results** - Highlight automated testing
5. **Check Swagger Docs** - Use the "Get API Docs" request

## Troubleshooting

### Connection Refused
- Ensure the FastAPI server is running: `uvicorn main:app --reload --port 8000`
- Verify the server is running from the correct directory: `artifacts/app`

### 500 Internal Server Error
- Check that the database file exists at `artifacts/onboarding.db`
- Review server logs for detailed error messages

### Environment Variable Not Found
- Make sure the environment is selected in the dropdown
- Run the "Create New User" request first to populate `created_user_id`

## API Documentation

For interactive API documentation, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running the Server

If the server is not running, start it with:

```bash
cd /path/to/AG-AISOFTDEV/artifacts/app
uvicorn main:app --reload --port 8000
```

The server will be available at http://localhost:8000