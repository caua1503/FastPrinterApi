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

FastPrinterAPI is a centralized system for managing multiple printers, focusing on statistics, forecasting, and detailed maintenance history. The project uses a monorepo architecture, containing both backend (API) and frontend (graphical interface) in a single repository for easier integration and maintenance.

## Objective

To facilitate the control, monitoring, and maintenance of printer fleets by providing:
- Real-time usage and status statistics
- Forecast of upcoming refills and cleanings
- Complete history of maintenance, refills, and events
- Management of departments, supplies, and users

## Key Features

- **Printer Management:** Register, update, query, and remove printers
- **Maintenance History:** Record and consult maintenance, refills, and cleanings
- **Intelligent Forecasting:** Calculation of the next refill/cleaning based on history
- **Departments:** Organization of printers by sectors
- **Multi-user System:** With control levels and access permissions
- **Secure Authentication:** Protected endpoints for sensitive operations using JWT
- **API System:** Flexible API system, allowing the creation of keys for one or multiple functions with different access levels
- **Permission System:** Flexible permission system (RBAC and ABAC) for both users and APIs

## Technologies Used

- Python 3.12+
- FastAPI (asynchronous)
- Postgres 17 (Database)
- Redis 8.0 (Cache database)
- Pydantic (data validation)
- Celery Python (Task executor and queue system)
- SQLAlchemy (ORM)
- Alembic (migrations)
- Docker (optional)

## Application Architecture

FastPrinterAPI uses a modular, scalable, and maintainable monorepo architecture, with backend and frontend organized in the same repository for clear separation of responsibilities and integrated development.

Directory structure:

```
impressoras/
  backend/    # Backend API (FastAPI, Celery, PostgreSQL, Redis, etc.)
  frontend/   # Frontend application (graphical interface, in development)
```

This approach allows better integration, unified versioning, and easier management of shared resources. Each module (backend and frontend) is self-contained, with its own dependencies and documentation, but both are part of the same project for streamlined development and deployment.

---

- For backend details, see: [backend/README.md](backend/README.md)
- For frontend details, see: [frontend/README.md](frontend/README.md)
- For full development and production guides, see [docs/en/](backend/docs/en/)