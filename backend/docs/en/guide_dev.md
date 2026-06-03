# Project Development Guide

This guide was created to help anyone who wants to contribute to the project or understand it, explaining everything from the environment setup to the architectural decisions I made.

## 1. Development Environment Setup

This project uses `uv` for dependency and virtual environment management. `uv` is a high-performance tool, similar to poetry, that speeds up package installation and management.

1.  **Install `uv`**: I recommend following the [official uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) to have the tool available on your system or install it via pip.
2.  **Synchronize dependencies**: After installing `uv`, navigate to the project root and run the following command to install all dependencies:
    ```bash
    uv sync
    ```

## 2. Useful Commands (Taskipy)

To facilitate development, I have configured some shortcuts with `taskipy`. Below are the available commands:

### Environment and Execution
- `task dev`: Starts the development environment using the `development.sh` script.
- `task windev`: Creates an environment, builds the Docker image, and starts the containers (optimized for Windows).
- `task build`: Builds the application's Docker image.
- `task rundocker`: Starts the services defined in `docker-compose.yaml` in detached mode.
- `task docker`: Executes the `build` and `rundocker` tasks in sequence.

### Code Quality and Testing
- `task lint`: Formats the code with `ruff` and applies automatic fixes.
- `task check`: Only checks the formatting and code quality with `ruff`.
- `task test`: Formats, checks, and runs the test suite with `pytest`.

### Migrations (Main Database)
- `task migrations`: Creates the initial migration structure with Alembic (use only once).
- `task update`: Generates a new migration file based on changes to the `models`.
- `task upgrade`: Applies pending migrations to the database.



## 3. Architectural Decisions and Patterns

### Layered Architecture
I sought to organize the project following a **Layered Architecture**. The idea is to separate the code based on its responsibilities to facilitate project maintenance and evolution.

- `app/routers`: Defines the API endpoints. It receives HTTP requests, validates the data with the `schemas`, and calls the corresponding service layer.
- `app/services`: Contains the application's business logic. It orchestrates operations and interacts with the data access layer.
- `app/models`: Defines the data models (tables) using SQLAlchemy ORM.
- `app/schemas`: Defines the data "contracts" with Pydantic, ensuring the validation and format of input and output data.
- `app/core`: Stores functionalities that are used in multiple places, such as security, background tasks (Celery), and logging.
- `app/helpers`: Contains utility functions to assist with specific tasks, such as database sessions, Redis manipulation, and data formatting.
- `app/config`: Centralizes the application's configurations, loaded from environment variables.

### Testing with Pytest
To ensure quality and stability, the project has a test suite with `pytest`. Test coverage aims to cover a large part of the code, helping to prevent regressions and unexpected errors. The test structure was designed with a focus on separation of responsibilities, using fixtures to isolate and configure test scenarios.

### Static Typing
Despite Python's dynamic typing, I chose to adopt **static typing** throughout the project. Tools like Pydantic and SQLAlchemy, which are already the basis for schemas and models, encourage this practice.

**Why I adopted static typing:**
- **Clarity**: Makes the code more readable and easier to understand.
- **Productivity**: Helps with intelligent autocompletion and IDE navigation.
- **Security**: Allows for safer refactoring and helps find errors even before running the code.
- **Documentation**: Serves as living and always up-to-date documentation.
- **Maintenance**: Simplifies maintenance, especially as the project grows. 