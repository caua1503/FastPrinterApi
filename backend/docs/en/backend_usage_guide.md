# Backend Usage Guide

This guide provides essential instructions on how to use the backend of the printer management system.

## Accessing the Interactive Documentation (Swagger UI)

The entire API is self-documented (thanks to FastAPI) following the OpenAPI standard.
You can access the Swagger UI interface to see all the project's endpoints, their parameters, and data models.

- **Access URL:** `http://<your-server>:<port>/docs`
- **Localhost URL:** `http://localhost:8000/docs`

Through the interface, you can:
- View all available endpoints.
- Understand what parameters each endpoint expects.
- Test the API in real-time by sending requests and viewing the responses.

## First Access and Authentication

For first-time use, a default administrator user is created so you can configure the system.

- **Login:** `fastprinter_admin`
- **Password:** `123456`

**Important:** For security reasons, it is recommended that you **change the password** of this user upon first login. The system may automatically prompt for a password change.

To authenticate, use the `/api/v1/auth/login` endpoint and send the credentials. The API will return an access token that must be used to authorize subsequent requests.

## Main API Features

The API is organized into routes that represent the main features of the system:

- `/users`: User management (create, read, update, delete).
- `/printers`: Printer management.
- `/supplies`: Supply control (toners, cartridges, etc.).
- `/departments`: Management of the organization's departments.
- `/history`: Record of maintenance histories, recharges, and other events.
- `/permissions`: Control of user access permissions and their API keys.

I recommend exploring each of these routes in the Swagger documentation to help understand how they work. 