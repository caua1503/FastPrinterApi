import asyncio
from typing import Any, Callable

from celery import Celery

from app.config import Config
from app.helpers.database_helper import get_session
from app.schemas.filter_schema import FilterBase
from app.schemas.logs_schema import ApiKeyLogSchema, SystemLogSchema, UserLogSchema

config = Config()  # pyright: ignore

celery_app = Celery(
    "celery_worker",
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/1",
)


@celery_app.task
def task_get_all_printers_maintenance_info():
    from app.core import get_all_printers_maintenance_info  # noqa: PLC0415

    async def __execute():
        async for session in get_session():
            printers_maintenance_info = await get_all_printers_maintenance_info(session, filters=FilterBase())
            return printers_maintenance_info

    return asyncio.run(__execute())


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_system_log(log: SystemLogSchema):
    from app.core.logs import create_system_log  # noqa: PLC0415
    try:
        asyncio.run(create_system_log(log))
    except Exception as e:
        raise e


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_user_log(log: UserLogSchema):
    from app.core.logs import create_user_log  # noqa: PLC0415
    try:
        asyncio.run(create_user_log(log))
    except Exception as e:
        raise e


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_api_key_log(log: ApiKeyLogSchema):
    from app.core.logs import create_api_key_log  # noqa: PLC0415
    try:
        asyncio.run(create_api_key_log(log))
    except Exception as e:
        raise e