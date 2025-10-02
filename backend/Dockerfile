FROM python:3.12-slim

WORKDIR /app/
COPY . .

RUN pip install --no-cache-dir uv
RUN uv venv && uv sync --no-dev && uv run --no-dev create_env.py -n

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]