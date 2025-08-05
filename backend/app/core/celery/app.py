from celery import Celery

from app.config import get_config

config = get_config()  # pyright: ignore

celery_app = Celery(
    "celery_worker",
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/1",
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
)
