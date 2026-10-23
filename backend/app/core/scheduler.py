import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_config
from app.helpers.database_helper import engine, get_session
from app.models.auth_model import RefreshToken
from app.schemas.filter_schema import FilterBase

config = get_config()  # pyright: ignore

logger = logging.getLogger(__name__)


async def job_update_all_printers_maintenance() -> None:
    """Atualiza as informações de manutenção de todas as impressoras.

    # TODO(etapa 3): revisar logica de manutencao
    """
    try:
        from app.services.maintenance_service import get_all_printers_maintenance_info  # noqa: PLC0415

        async for session in get_session():
            await get_all_printers_maintenance_info(session, filters=FilterBase())
    except Exception:
        logger.exception("Erro ao executar job_update_all_printers_maintenance")


async def job_clean_refresh_tokens() -> None:
    """Remove refresh tokens expirados (mais de 20 dias) do banco de dados."""
    try:
        expiration_date = datetime.now() - timedelta(days=20)
        async with AsyncSession(engine) as session:
            result = await session.execute(delete(RefreshToken).where(RefreshToken.expires_at < expiration_date))
            await session.commit()
            logger.info("Refresh tokens removidos: %d", result.rowcount)
    except Exception:
        logger.exception("Erro ao executar job_clean_refresh_tokens")


def create_scheduler() -> AsyncIOScheduler:
    """Cria e configura o AsyncIOScheduler com os jobs de manutenção e limpeza.

    Returns:
        AsyncIOScheduler: Scheduler configurado, pronto para ser iniciado.
                          Não inicia o scheduler na importação.
    """
    scheduler = AsyncIOScheduler(
        timezone=config.TIMEZONE,
        job_defaults={
            "max_instances": 1,
            "coalesce": True,
            "misfire_grace_time": 3600,
        },
    )

    scheduler.add_job(
        job_update_all_printers_maintenance,
        trigger=CronTrigger(hour=2, minute=0, timezone=config.TIMEZONE),
        id="update_all_printers_maintenance",
        replace_existing=True,
    )

    scheduler.add_job(
        job_clean_refresh_tokens,
        trigger=CronTrigger(hour=3, minute=0, day=1, timezone=config.TIMEZONE),
        id="clean_refresh_tokens",
        replace_existing=True,
    )

    return scheduler
