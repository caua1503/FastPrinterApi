import asyncio
from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.celery.app import celery_app
from app.helpers.database_helper import get_session
from app.models.auth_model import RefreshToken
from app.schemas.filter_schema import FilterBase


@celery_app.task
def task_get_all_printers_maintenance_info():
    from app.core import get_all_printers_maintenance_info  # noqa: PLC0415

    async def __execute():
        async for session in get_session():
            printers_maintenance_info = await get_all_printers_maintenance_info(session, filters=FilterBase())
            return printers_maintenance_info

    return asyncio.run(__execute())


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
