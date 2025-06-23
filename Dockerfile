FROM python:3.12-slim

WORKDIR app/
COPY . .

RUN pip install --no-cache-dir uv
RUN uv venv && uv sync --no-dev
RUN python .\create_env.py -n 
RUN alembic -c alembic.ini upgrade head && alembic -c alembic_logs.ini upgrade head

EXPOSE 8000

CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--workers", "2", "--port", "8000", "app.main:app"]