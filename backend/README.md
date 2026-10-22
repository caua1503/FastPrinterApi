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
    core/             # Core components: security, standalone scheduler (APScheduler)
    helpers/          # Helper modules (e.g., Redis connection, utilities)
    models/           # ORM data models (SQLAlchemy)
    routers/api/      # API endpoints, organized by resource
    schemas/          # Data validation schemas (Pydantic)
    services/         # Business logic, decoupled from endpoints
    scheduler_main.py # Standalone scheduler entrypoint (APScheduler 3.x)
  migrations/         # Main database migrations (Alembic)

  test/               # Automated tests (Pytest)
  compose.yaml        # Service orchestration with Docker
  create_env.py       # Script to generate the .env environment file
  init_db.py          # Script to initialize the database with default data
```

## Scheduling Service (APScheduler)

Scheduled jobs run in a separate process via:
```bash
uv run python -m app.scheduler_main
```

- **Timezone**: Configured via `TIMEZONE` in `.env` (default: `America/Sao_Paulo`).
- **Jobs**:
  - `update_all_printers_maintenance`: Runs daily at 02:00.
  - `clean_refresh_tokens`: Runs on the 1st of every month at 03:00.

## Documentation

📖 See the [development guide](docs/en/guide_dev.md) for architectural decisions
