import asyncio
from datetime import datetime
from typing import Optional, Tuple, Type, Union

from redis.exceptions import AuthenticationError, ConnectionError, TimeoutError

from app.core.celery.app import celery_app
from app.helpers.database_helper import get_session_logs
from app.models.logs_model import ApiKeyLog, SystemLog, UserLog
from app.schemas.logs_schema import ApiKeyLogSchema, LogLevelSchema, ServiceSchema, SystemLogSchema, UserLogSchema

# Tipagem explícita para o dicionário de criadores de log
LOG_CREATORS = {
    "system": (SystemLogSchema, SystemLog),
    "user": (UserLogSchema, UserLog),
    "api_key": (ApiKeyLogSchema, ApiKeyLog),
}


def get_log_classes(log_type: str) -> Tuple[Type, Type]:
    """
    Retorna as classes de schema e model para o tipo de log informado.
    """
    try:
        return LOG_CREATORS[log_type]
    except KeyError:
        raise ValueError(f"Tipo de log inválido: {log_type}")


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 6, "countdown": 15})
def task_create_log(self, log_type: str, **log_data):
    """
    Task unificada para criação de logs.
    Args:
        log_type: Tipo do log ('system', 'user', 'api_key')
        **log_data: Dados do log a serem criados
    """
    schema_class, _ = get_log_classes(log_type)
    log = schema_class(**log_data)
    asyncio.run(create_log(log_type, log))


async def create_log(log_type: str, log: Union[SystemLogSchema, UserLogSchema, ApiKeyLogSchema]):
    """
    Função unificada para criação de logs no banco de dados.
    Args:
        log_type: Tipo do log ('system', 'user', 'api_key')
        log: Instância do schema do log
    """
    _, model_class = get_log_classes(log_type)
    async for session in get_session_logs():
        log_data = log.model_dump()
        log_db = model_class(**log_data)
        session.add(log_db)
        await session.commit()
        await session.refresh(log_db)


async def create_redis_log(erro: Exception, level_log: Optional[LogLevelSchema] = None):
    """
    Cria logs específicos para erros do Redis.
    Utiliza a nova função unificada internamente.
    """
    if isinstance(erro, ConnectionError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Connection error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        task_create_log.delay("system", **erro_log.model_dump())

    elif isinstance(erro, TimeoutError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Timeout error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        task_create_log.delay("system", **erro_log.model_dump())

    elif isinstance(erro, AuthenticationError):
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Authentication error",
            level=LogLevelSchema.CRITICAL,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        task_create_log.delay("system", **erro_log.model_dump())

    else:
        erro_log = SystemLogSchema(
            message=str(erro),
            description="Unknown Redis error",
            level=LogLevelSchema.WARNING if level_log is None else level_log,
            service=ServiceSchema.REDIS,
            timestamp=datetime.now(),
        )
        task_create_log.delay("system", **erro_log.model_dump())
