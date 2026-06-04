# FastPrinterAPI Backend

## Technologies Used (Development)

- Automated tests (pytest)
- Linter and code formatter (Ruff)
- Complementary task runner (Taskipy)

📖 See the documentation to run in [development mode](docs/en/development.md)

## Folder Structure & Responsibilities

The backend is organized to ensure modularity, scalability, and maintainability, following a layered architecture and clear separation of concerns:

```
backend/
  app/
    config/           # Settings and environment variables (via Pydantic)
    core/             # Core components: security, background tasks (Celery), logging
    helpers/          # Helper modules (e.g., Redis connection, utilities)
    models/           # ORM data models (SQLAlchemy)
    routers/api/      # API endpoints, organized by resource
    schemas/          # Data validation schemas (Pydantic)
    services/         # Business logic, decoupled from endpoints
  migrations/         # Main database migrations (Alembic)

  test/               # Automated tests (Pytest)
  celery_worker.py    # Celery worker and task scheduler definition
  compose.yaml        # Service orchestration with Docker
  create_env.py       # Script to generate the .env environment file
  init_db.py          # Script to initialize the database with default data
```

## Documentation

📖 See the [development guide](docs/en/guide_dev.md) for architectural decisions
