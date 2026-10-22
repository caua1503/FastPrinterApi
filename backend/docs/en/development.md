## Getting Started (for development)

Follow these instructions to set up and run the project in your local development environment.

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- `uv` (Python package installer)

This project uses `uv` for package management and virtual environments. Its installation is **required**.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/caua1503/FastPrinterApi.git
    cd FastPrinterAPI
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    # Install UV (if you don't have it yet)
    pip install uv
    # or follow the instructions at: https://docs.astral.sh/uv/getting-started/installation/

    # Create the virtual environment
    uv venv

    # Activate the virtual environment
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate

    # Install/sync dependencies
    uv sync
    ```

## Running Tests

To ensure the quality and integrity of the code, run the automated test suite:

```bash
uv run python create_env.py --no_interative
task test
```

This command will format the code, check for linting errors, and then run the tests with `pytest`.

## Running the Application

You can run the application in two ways: with Docker or locally.

### 1. With Docker

**Step 1: Adjust the execution mode for development**

Before starting the containers, you need to modify the `entrypoint.sh` file so that the application runs in development mode (with auto-reloading) and initializes the database.

Open the `entrypoint.sh` file and make the following changes:

```diff
# Start FastAPI server
log "Starting FastAPI server..."

# Comment out the production line (granian or uvicorn)
# uv run --no-dev uvicorn app.main:app --host 0.0.0.0 --port 8000

# And uncomment the development line (fastapi dev)
uv run --no-dev fastapi dev --port 8000 --host 0.0.0.0 --reload ./app
```

**Step 2: Start the containers**

After saving the changes to `entrypoint.sh`, run the following command to create the `.env` file, build the Docker image, and start the services:

```bash
task windev
```
The services (application, scheduler, database, and Redis) will be running in the background. The server will be available at `http://localhost:8000/docs`.

### 2. Locally

If you are running the application locally, you can use the development script that automates the whole process.

**How to run:**

In a terminal, with Docker running and the virtual environment activated, run:
```bash
task dev
```

This command will do the following:
1.  Verify that Docker is running.
2.  Create the `.env` file with defaults if it does not exist.
3.  Start Docker containers for PostgreSQL and Redis.
4.  Run database migrations.
5.  Initialize database with default data.
6.  Start the FastAPI server and the scheduling service (`uv run python -m app.scheduler_main`) in the background.

The server will be available at `http://127.0.0.1:8000/docs`. To stop all processes, simply press `Ctrl+C` in the terminal.

### Standalone Scheduler Service (APScheduler)

Task scheduling is decoupled from the API process and powered by **APScheduler 3.x** (`AsyncIOScheduler`), running in a separate process:

```bash
uv run python -m app.scheduler_main
```

- **Environment Variable `TIMEZONE`**: Sets the timezone for cron triggers (default: `America/Sao_Paulo`).
- **Registered Jobs**:
  - `update_all_printers_maintenance`: Runs daily at 02:00 to update maintenance forecasts for all printers.
  - `clean_refresh_tokens`: Runs on the 1st of every month at 03:00 to purge refresh tokens expired for more than 20 days. 