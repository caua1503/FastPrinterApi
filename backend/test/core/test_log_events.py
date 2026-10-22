"""Testes para app.core.log_events.

Nota: Como o banco de dados de logs foi removido (commit ed744ea),
estes testes verificam apenas o comportamento básico do stub.
"""

import asyncio

import pytest

from app.core import log_events
from app.core.log_events import log_event, log_redis_error


@pytest.mark.asyncio
async def test_log_event_runs_without_exception():
    """log_event() não deve lançar exceção em contexto asyncio."""
    log_event("system", message="teste")
    # Aguarda as tasks em background terminarem
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_log_event_task_removed_from_set_after_completion():
    """A task deve ser removida do _background_tasks após completar."""
    initial_count = len(log_events._background_tasks)  # noqa: SLF001
    log_event("system", message="teste_set")
    # Aguarda a task terminar e ser removida do set
    await asyncio.sleep(0.2)
    assert len(log_events._background_tasks) <= initial_count, "Tasks devem ser removidas do set ao completar"  # noqa: SLF001


@pytest.mark.asyncio
async def test_log_redis_error_runs_without_exception():
    """log_redis_error() não deve lançar exceção."""
    log_redis_error(Exception("erro simulado de redis"), level_log="error")
    await asyncio.sleep(0.1)


def test_log_event_outside_event_loop_does_not_raise():
    """log_event() fora de um event loop não deve lançar exceção."""
    # Executado fora de asyncio.run, sem loop ativo
    log_event("system", message="sem loop")
