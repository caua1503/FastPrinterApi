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

### 1. With Docker (Recommended for Windows)

This approach is recommended for development on Windows, as Celery (the background task manager) has dependencies that are not natively compatible with this system.

**Step 1: Adjust the execution mode for development**

Before starting the containers, you need to modify the `entrypoint.sh` file so that the application runs in development mode (with auto-reloading) and initializes the database.

Open the `entrypoint.sh` file and make the following changes:

```diff
# Start FastAPI server
log "Starting FastAPI server..."

# Comment out the production line (granian)
# uv run --no-dev granian --interface asgi --host 0.0.0.0 --workers 1 --port 8000 app.main:app

# And uncomment the development line (fastapi dev)
uv run --no-dev fastapi dev --port 8000 --host 0.0.0.0 --reload ./app
```

**Step 2: Start the containers**

After saving the changes to `entrypoint.sh`, run the following command to create the `.env` file, build the Docker image, and start the services:

```bash
task windev
```
The services (application, database, Redis, and Celery) will be running in the background. The server will be available at `http://localhost:8000/docs`.

### 2. Locally (Linux/macOS only)

If you are on a Linux or macOS environment, you can run the application directly. With a single command, you can start the FastAPI server and Celery processes in the background.

**How to run:**

In a terminal, with the virtual environment activated, run:
```bash
task dev
```

This command will do the following:
1.  Start the **Celery Worker** in the background.
2.  Start the **Celery Beat** (scheduler) in the background.
3.  Start the **FastAPI** server in development mode, which will remain active in your terminal.

The server will be available at `http://127.0.0.1:8000/docs`. To stop all processes, simply press `Ctrl+C` in the terminal. 