FROM python:3.12-slim

WORKDIR app/
COPY . .

RUN pip install --no-cache-dir uv
RUN uv venv && uv sync --no-dev

EXPOSE 8000

CMD ["/app/.venv/bin/granian", "--interface", "asgi", "--host", "0.0.0.0", "--workers", "2", "--port", "8000", "app.main:app"]