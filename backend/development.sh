#!/bin/bash

# Exit script on error
set -e

# --- Settings ---
DB_USER="postgres"
DB_PASSWORD="password"
DB_NAME="postgres"
DB_PORT="5432"

REDIS_PORT="6379"

POSTGRES_CONTAINER_NAME="postgres-dev"

REDIS_CONTAINER_NAME="redis-dev"

# --- Helper Functions ---
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

start_container() {
    local name="$1"
    local image="$2"
    local port_mapping="$3"
    local env_vars="$4"

    if ! docker ps -a --format '{{.Names}}' | grep -q "^${name}$"; then
        echo "Creating and starting container: ${name}"
        docker run -d --name "${name}" -p "${port_mapping}" ${env_vars} "${image}"
    elif ! docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        echo "Starting existing container: ${name}"
        docker start "${name}"
    else
        echo "Container ${name} is already running."
    fi
}

# --- Main Script ---

# Parse command-line options
INIT_DB_ARGS=""
LANGUAGE_MESSAGE="default (English)"
while getopts "p" opt; do
  case ${opt} in
    p )
      INIT_DB_ARGS="-p"
      LANGUAGE_MESSAGE="Portuguese"
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# 1. Check dependencies
if ! command_exists docker; then
    echo "Error: Docker is not installed. Please install it to continue."
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start it to continue."
    exit 1
fi

# 2. Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file with default values..."
    uv run python create_env.py --no_interative
else
    echo ".env file already exists."
fi

# 3. Start services with Docker
echo "Starting Docker containers..."
start_container "${POSTGRES_CONTAINER_NAME}" "postgres:17" "${DB_PORT}:5432" "-e POSTGRES_USER=${DB_USER} -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_DB=${DB_NAME}"

start_container "${REDIS_CONTAINER_NAME}" "redis:8.0" "${REDIS_PORT}:6379" ""

echo "Waiting for services to be ready..."
sleep 5 # Simple wait, could be improved with health checks

# 4. Run database migrations
echo "Running database migrations..."
uv run alembic -c alembic.ini upgrade head


# 5. Initialize database with default data
echo "Initializing database with $LANGUAGE_MESSAGE data..."
uv run python init_db.py $INIT_DB_ARGS

# 6. Start application components
echo "Starting the application..."
trap 'kill $(jobs -p)' EXIT

uv run fastapi dev ./app &
uv run celery -A celery_worker worker --loglevel=info &
uv run celery -A celery_worker beat --loglevel=info &

wait
