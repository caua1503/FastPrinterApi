import asyncio
from datetime import datetime, timedelta

from celery import Celery
from sqlalchemy import select

from app.config import get_config
from app.helpers.database_helper import get_session
from app.models.auth_model import RefreshToken
from app.schemas.filter_schema import FilterBase
from app.schemas.logs_schema import ApiKeyLogSchema, SystemLogSchema, UserLogSchema

config = get_config()  # pyright: ignore

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
def task_create_system_log(self, **log_data):
    from app.core.logs import create_system_log  # noqa: PLC0415

    try:
        log = SystemLogSchema(**log_data)
        asyncio.run(create_system_log(log))
    except Exception as e:
        raise e


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_user_log(self, **log_data):
    from app.core.logs import create_user_log  # noqa: PLC0415

    try:
        log = UserLogSchema(**log_data)
        asyncio.run(create_user_log(log))
    except Exception as e:
        raise e


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_api_key_log(self, **log_data):
    from app.core.logs import create_api_key_log  # noqa: PLC0415

    try:
        log = ApiKeyLogSchema(**log_data)
        asyncio.run(create_api_key_log(log))
    except Exception as e:
        raise e


@celery_app.task()
def task_clean_refresh_token_database():
    async def __execute():
        expiration_date = datetime.now() - timedelta(days=20)
        async for session in get_session():
            tokens = (
                await session.scalars(select(RefreshToken).where((RefreshToken.expires_at < expiration_date)))
            ).all()

            for token in tokens:
                await session.delete(token)
            await session.commit()

    return asyncio.run(__execute())
