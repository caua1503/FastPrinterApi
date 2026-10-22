"""Módulo de eventos de log assíncronos.

Nota: O banco de dados de logs secundário foi removido no commit ed744ea.
Este módulo mantém a interface pública para futura reimplementação (etapa futura).
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

# Mantém referências fortes às tasks para evitar coleta antes de terminar
_background_tasks: set[asyncio.Task] = set()


async def _safe_noop(log_type: str, log_data: dict) -> None:
    """Placeholder: grava nada (banco de logs removido)."""
    logger.debug("log_event ignorado (sem banco de logs): type=%s data=%s", log_type, log_data)


def log_event(log_type: str, **log_data) -> None:
    """Agenda a gravação do log em background, sem bloquear a requisição.

    Atualmente é um stub: o banco de dados de logs foi removido.
    Reimplementar quando o banco de logs for restaurado.
    """
    try:
        loop = asyncio.get_running_loop()
        task = loop.create_task(_safe_noop(log_type, log_data))
        _background_tasks.add(task)
        task.add_done_callback(_background_tasks.discard)
    except RuntimeError:
        # Fora de um event loop — ignorar silenciosamente
        pass


def log_redis_error(erro: Exception, level_log: str | None = None) -> None:
    """Registra um erro de Redis em background.

    Atualmente é um stub: o banco de dados de logs foi removido.
    """
    log_event("redis_error", error=str(erro), level_log=level_log)
