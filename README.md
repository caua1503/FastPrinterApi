# FastPrinterAPI

📖 Read this documentation in [Portuguese](README.pt-BR.md)

<p align="center">
  <a href="https://www.python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
  <a href="https://www.postgresql.org" target="_blank">
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://redis.io" target="_blank">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
</p>

An asynchronous API developed in FastAPI for centralized management of multiple printers, focusing on statistics, forecasts, and detailed maintenance history.

Although the core of the project is the RESTful API, it will also include an intuitive graphical interface to facilitate interaction and management (coming soon).

## Objective

To facilitate the control, monitoring, and maintenance of printer fleets by providing:
- Real-time usage and status statistics
- Forecast of upcoming refills and cleanings
- Complete history of maintenance, refills, and events
- Management of departments, supplies, and users

## Key Features

- **Printer Management:** Register, update, query, and remove printers.
- **Maintenance History:** Record and consult maintenance, refills, and cleanings.
- **Intelligent Forecasting:** Calculation of the next refill/cleaning based on history.
- **Departments:** Organization of printers by sectors.
- **Multi-user System:** With control levels and access permissions.
- **Secure Authentication:** Protected endpoints for sensitive operations using JWT.
- **API System:** Flexible API system, allowing the creation of keys for one or multiple functions with different access levels.
- **Permission System:** Flexible permission system (RBAC and ABAC) for both users and APIs.

## Technologies Used (Production)

- Python 3.12+
- FastAPI (asynchronous)
- Postgres 17 (Database)
- Redis 8.0 (Cache database)
- Pydantic (data validation)
- Celery Python (Task executor and queue system)
- SQLAlchemy (ORM)
- Alembic (migrations)
- Docker (optional)

📖 Read the documentation to run in [production](docs/en/production.md) mode 

## Technologies Used (Development)

- Automated tests (pytest)
- Linter and code formatter (Ruff)
- Complementary task runner (Taskipy)

📖 Read the documentation to run in [development](docs/en/development.md) mode 

## Application Architecture

The FastPrinterAPI architecture was designed to be modular, scalable, and easy to maintain, following the best practices for API development with FastAPI. The directory structure reflects a clear separation of responsibilities:

```
FastPrinterAPi/
  app/
    config/           # Settings and environment variables (via Pydantic)
    core/             # Core components: security, background tasks (Celery)
    helpers/          # Helper modules (e.g., Redis connection, utilities)
    models/           # ORM data models (SQLAlchemy)
    routers/api/      # API endpoints, organized by resource
    schemas/          # Data validation schemas (Pydantic)
    services/         # Business logic, decoupled from endpoints
  migrations/         # Main database migrations (Alembic)
  migrations_logs/    # Log database migrations (Alembic)
  test/               # Automated tests (Pytest)
  celery_worker.py    # Worker definition and task scheduling (Celery Beat)
  compose.yaml        # Service orchestration with Docker
  create_env.py       # Script to generate the .env environment file
  init_db.py          # Script to initialize the database with default data
  ...
```

📖 Read the [development guide](docs/en/guide_dev.md) to understand architectural decisions