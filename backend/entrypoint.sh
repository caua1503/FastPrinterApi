#!/bin/bash

# Function for logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command was executed successfully
check_error() {
    if [ $? -ne 0 ]; then
        log "ERROR: $1"
        exit 1
    fi
}

# Wait for the database to be ready
log "Waiting for database..."
sleep 5

# Execute migrations for the main database
log "Executing migrations for the main database..."
uv run --no-dev alembic -c alembic.ini upgrade head
check_error "Main database migrations failed"


# Initialize database
log "Initializing database..."
uv run --no-dev init_db.py  #use -p para inicializar em portugues

# Start Celery worker in background
log "Starting Celery worker..."
uv run --no-dev celery -A celery_worker worker --loglevel=warning &
uv run --no-dev celery -A celery_worker beat --loglevel=warning &

# Start FastAPI server
log "Starting FastAPI server..."
uv run --no-dev uvicorn app.main:app --host 0.0.0.0 --port 8000
# uv run --no-dev fastapi dev --port 8000 --host 0.0.0.0 --reload ./app