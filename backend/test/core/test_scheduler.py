from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
import pytest_asyncio
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import scheduler as scheduler_module
from app.core.scheduler import create_scheduler, job_clean_refresh_tokens, job_update_all_printers_maintenance
from app.models.auth_model import RefreshToken
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.user_model import User
from app.schemas.user_schema import UsersRoleSchema

# ── constantes ────────────────────────────────────────────────────────────────
EXPECTED_JOB_COUNT = 2
EXPECTED_MISFIRE_GRACE_TIME = 3600


# ── fixtures ──────────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    """Cria um usuário mínimo para vincular RefreshTokens."""
    u = User(
        login="testuser_scheduler",
        password_hash="hashed",
        name="Test User",
        role=UsersRoleSchema.member,
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def old_token(session: AsyncSession, user):
    """Token expirado há mais de 20 dias — deve ser removido."""
    token = RefreshToken(
        token="old_token_value",
        user_id=user.id,
        expires_at=(datetime.now(timezone.utc) - timedelta(days=25)).replace(tzinfo=None),
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token


@pytest_asyncio.fixture
async def recent_token(session: AsyncSession, user):
    """Token ainda válido — NÃO deve ser removido."""
    token = RefreshToken(
        token="recent_token_value",
        user_id=user.id,
        expires_at=(datetime.now(timezone.utc) + timedelta(days=7)).replace(tzinfo=None),
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token


# ── tests ─────────────────────────────────────────────────────────────────────


def test_create_scheduler_registers_two_jobs():
    """create_scheduler() deve registrar exatamente os 2 jobs esperados."""
    scheduler = create_scheduler()
    jobs = {job.id: job for job in scheduler.get_jobs()}

    assert len(jobs) == EXPECTED_JOB_COUNT, f"Esperado {EXPECTED_JOB_COUNT} jobs, encontrado: {list(jobs.keys())}"
    assert "update_all_printers_maintenance" in jobs
    assert "clean_refresh_tokens" in jobs


@pytest.mark.asyncio
async def test_scheduler_job_defaults():
    """Os job_defaults devem ter max_instances=1 e coalesce=True (verificado após start)."""
    scheduler = create_scheduler()
    scheduler.start()
    try:
        jobs = {job.id: job for job in scheduler.get_jobs()}
        for job_id, job in jobs.items():
            assert job.max_instances == 1, f"{job_id}: max_instances deve ser 1"
            assert job.coalesce is True, f"{job_id}: coalesce deve ser True"
            assert job.misfire_grace_time == EXPECTED_MISFIRE_GRACE_TIME, (
                f"{job_id}: misfire_grace_time deve ser {EXPECTED_MISFIRE_GRACE_TIME}"
            )
    finally:
        scheduler.shutdown(wait=False)


def test_scheduler_maintenance_job_trigger():
    """O job de manutenção deve disparar todos os dias às 02:00."""
    scheduler = create_scheduler()
    jobs = {job.id: job for job in scheduler.get_jobs()}
    job = jobs["update_all_printers_maintenance"]

    assert isinstance(job.trigger, CronTrigger)
    fields = {field.name: field for field in job.trigger.fields}
    assert str(fields["hour"]) == "2", "hora deve ser 2"
    assert str(fields["minute"]) == "0", "minuto deve ser 0"


def test_scheduler_clean_tokens_job_trigger():
    """O job de limpeza deve disparar no dia 1 de cada mês às 03:00."""
    scheduler = create_scheduler()
    jobs = {job.id: job for job in scheduler.get_jobs()}
    job = jobs["clean_refresh_tokens"]

    assert isinstance(job.trigger, CronTrigger)
    fields = {field.name: field for field in job.trigger.fields}
    assert str(fields["hour"]) == "3", "hora deve ser 3"
    assert str(fields["minute"]) == "0", "minuto deve ser 0"
    assert str(fields["day"]) == "1", "dia deve ser 1"


@pytest.mark.asyncio
async def test_job_clean_refresh_tokens_removes_old(session: AsyncSession, old_token, recent_token):
    """job_clean_refresh_tokens() deve remover tokens com expires_at < 20 dias atrás."""
    original_engine = scheduler_module.engine

    # Usa o engine da sessão de teste
    scheduler_module.engine = session.bind  # type: ignore[assignment]

    try:
        await job_clean_refresh_tokens()

        remaining = (await session.scalars(select(RefreshToken))).all()
        remaining_tokens = [t.token for t in remaining]

        assert "old_token_value" not in remaining_tokens, "Token expirado deve ter sido removido"
        assert "recent_token_value" in remaining_tokens, "Token recente deve ter sido mantido"
    finally:
        scheduler_module.engine = original_engine


@pytest.mark.asyncio
async def test_job_update_all_printers_maintenance_runs_without_exception(session: AsyncSession, printer):
    """job_update_all_printers_maintenance() deve rodar sem exceção com uma impressora existente."""

    async def _patched_get_session():
        yield session

    with patch("app.core.scheduler.get_session", _patched_get_session):
        # Deve completar sem lançar exceção
        await job_update_all_printers_maintenance()

    # Verifica que PrinterMaintenanceInfo foi criado/atualizado
    result = await session.scalar(select(PrinterMaintenanceInfo).where(PrinterMaintenanceInfo.printer_id == printer.id))
    assert result is not None, "PrinterMaintenanceInfo deve ter sido criado para a impressora"


@pytest.mark.asyncio
async def test_job_exception_does_not_propagate():
    """Uma falha dentro de um job NÃO deve propagar a exceção para o scheduler."""
    with patch("app.core.scheduler.get_session", side_effect=RuntimeError("simulando falha")):
        # Não deve lançar exceção
        await job_update_all_printers_maintenance()

    with patch("app.core.scheduler.AsyncSession", side_effect=RuntimeError("simulando falha no delete")):
        await job_clean_refresh_tokens()
