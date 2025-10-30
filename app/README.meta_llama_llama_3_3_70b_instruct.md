# Employee Onboarding Tool API
## Overview
The Employee Onboarding Tool API is designed to streamline and standardize the new hire experience. It provides a single source of truth for onboarding, empowering HR, equipping managers, and exciting new hires.

## Architecture & Tech Stack
The API is built using FastAPI and integrates with a SQLite database. It utilizes SQLAlchemy for database operations and Pydantic for schema validation.

## Features
The API supports the following features, mapped from the PRD epics:
- HR Admin: Create and manage standardized onboarding templates, populate the onboarding hub with company-wide resources, and track completion rates for mandatory compliance tasks.
- Hiring Manager: View progress of new hire's pre-boarding tasks, assign an onboarding buddy, create a structured first-week schedule, and receive automated reminders for check-ins.
- New Hire Journey: Complete pre-boarding paperwork, access a centralized onboarding hub, view detailed schedule for the first week, and receive a digital welcome packet.

## Data Model
The data model consists of the following high-level entities and relationships:
- User: Represents an employee with attributes like full_name, email, sso_identifier, role, manager_id, and hire_date.
- Template: Standardized onboarding templates created by HR.
- TemplateTask: Tasks associated with a template.
- OnboardingPlan: A plan assigned to a new hire, derived from a template.
- AssignedTask: Tasks assigned to a new hire as part of their onboarding plan.
- Resource: Company-wide resources available in the onboarding hub.
- ScheduleEvent: Events scheduled for a new hire, such as meetings and training sessions.
- SurveyResponse: Feedback collected from new hires.

## API Endpoints
The API provides the following endpoints:
- **/**: Returns a welcome message for the API root.
  - `curl http://localhost:8000/`
- **/users/**: Create a new user.
  - `curl -X POST -H "Content-Type: application/json" -d '{"full_name": "John Doe", "email": "john@example.com", "sso_identifier": "johndoe", "role": "employee", "manager_id": 1, "hire_date": "2022-01-01"}' http://localhost:8000/users/`
- **/users/**: Retrieve a list of all users.
  - `curl http://localhost:8000/users/`
- **/users/{user_id}**: Retrieve a single user by their ID.
  - `curl http://localhost:8000/users/1`
- **/users/{user_id}**: Update an existing user's details.
  - `curl -X PUT -H "Content-Type: application/json" -d '{"full_name": "Jane Doe"}' http://localhost:8000/users/1`
- **/users/{user_id}**: Delete a user from the system.
  - `curl -X DELETE http://localhost:8000/users/1`

## Request/Response Schemas
The API uses the following schemas:
- **UserCreate**: Represents data required to create a new user, including full_name, email, sso_identifier, role, manager_id, and hire_date.
- **UserUpdate**: Represents data to update an existing user, allowing for partial updates.
- **UserResponse**: Represents the response data for a user, including all attributes.

## Installation & Setup
To install and set up the API, follow these steps:
1. Clone the repository.
2. Install dependencies using pip.
3. Configure the database connection.

## Running the Application
To run the application, use the following command:
`uvicorn main:app --host 0.0.0.0 --port 8000`

## Database Initialization & Migration Notes
The database is initialized with the following tables: users, templates, template_tasks, onboarding_plans, assigned_tasks, resources, schedule_events, and survey_responses. The database path is set to sqlite:///database/onboarding.db.

## Configuration
The API uses environment variables for configuration. The database path can be specified using the SQLALCHEMY_DATABASE_URL variable.

## Error Handling & Status Codes
The API uses standard HTTP status codes for error handling, including 201 Created, 400 Bad Request, and 404 Not Found.

## Security & Non-Functional Requirements
The API adheres to the following non-functional requirements:
- Performance: Key pages load in under 3 seconds.
- Security: Integrates with the company's SSO provider, encrypts PII, and enforces RBAC.
- Accessibility: Compliant with WCAG 2.1 Level AA standards.
- Scalability: Supports up to 1,000 new hires being onboarded concurrently per quarter.
- Reliability: Maintains 99.9% uptime.
- Usability: The interface is intuitive and requires no formal training.

## Testing
The API includes unit tests and integration tests to ensure functionality and reliability.

## Roadmap & Release Plan
The API has the following release phases:
- Version 1.0: Establishing a single, consistent path for all new hires.
- Version 1.1: Enhanced manager and team tooling.
- Version 1.2: Analytics and process improvement.

## Future Enhancements
Future enhancements include:
- Integration with the corporate Learning Management System (LMS).
- AI-powered onboarding journeys.
- Deeper HRIS integration.
- Social features.

## Contributing
Contributions are welcome. Please submit a pull request with your changes.

## License
License TBD.