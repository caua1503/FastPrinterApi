from datetime import datetime
from typing import Optional

from redis.exceptions import AuthenticationError, ConnectionError, TimeoutError

from app.core.task import task_create_system_log
from app.helpers.database_helper import get_session_logs
from app.models.logs_model import SystemLog, UserLog
from app.schemas.logs_schema import LogLevelSchema, ServiceSchema, SystemLogSchema, UserLogSchema


async def create_user_log(log: UserLogSchema):
    async for session in get_session_logs():
        log_db = UserLog(
            user_id=log.user_id,
            message=log.message,
            level=log.level,
            service=log.service,
            timestamp=log.timestamp,
            description=log.description,
        )
        session.add(log_db)
        await session.commit()


async def create_system_log(log: SystemLogSchema):
    async for session in get_session_logs():
        log_db = SystemLog(
            message=log.message,
            description=log.description,
            level=log.level,
            service=log.service,
            timestamp=log.timestamp,
        )
        session.add(log_db)
        await session.commit()


async def create_redis_log(erro: Exception, level_log: Optional[LogLevelSchema] = None):
    if isinstance(erro, ConnectionError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Connection error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        await task_create_system_log.delay(erro_log)

    elif isinstance(erro, TimeoutError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Timeout error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        await task_create_system_log.delay(erro_log)

    elif isinstance(erro, AuthenticationError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Authentication error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        await task_create_system_log.delay(erro_log)

    else:
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Unknown Redis error",
            level=LogLevelSchema.WARNING if level_log is None else level_log,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        await task_create_system_log.delay(erro_log)
