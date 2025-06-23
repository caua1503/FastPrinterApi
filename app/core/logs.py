from datetime import datetime

from redis.exceptions import AuthenticationError, ConnectionError, TimeoutError

from app.schemas.logs_schema import LogLevel, SystemLog, UserLog


async def create_user_log(log: UserLog): ...


async def create_system_log(log: SystemLog): ...


async def create_redis_log(erro: Exception):
    if isinstance(erro, ConnectionError):
        erro_log = SystemLog(
            message=str(erro),
            description="Connection error",
            level=LogLevel.CRITICAL,
            service="Redis",
            timestamp=datetime.now(),
        )
        await create_system_log(erro_log)

    elif isinstance(erro, TimeoutError):
        erro_log = SystemLog(
            message=str(erro),
            description="Timeout error",
            level=LogLevel.CRITICAL,
            service="Redis",
            timestamp=datetime.now(),
        )
        await create_system_log(erro_log)

    elif isinstance(erro, AuthenticationError):
        erro_log = SystemLog(
            message=str(erro),
            description="Authentication error",
            level=LogLevel.CRITICAL,
            service="Redis",
            timestamp=datetime.now(),
        )
        await create_system_log(erro_log)

    else:
        erro_log = SystemLog(
            message=str(erro),
            level=LogLevel.WARNING,
            service="Redis",
            timestamp=datetime.now(),
        )
        await create_system_log(erro_log)
