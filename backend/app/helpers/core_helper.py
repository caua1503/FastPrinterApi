from datetime import date, timedelta
from statistics import mean, median
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.history_model import AlertHistory, PrinterTrashHistory, RefillHistory
from app.schemas.filter_schema import FilterBase
from app.schemas.history_schema import AlertHistorySchema


async def create_history_alert_core(history: AlertHistorySchema, session: AsyncSession) -> AlertHistorySchema:
    history_db = AlertHistory(
        printer_id=history.printer_id,
        date=history.date,
        alert_type=history.alert_type,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)

    return AlertHistorySchema(
        printer_id=history_db.printer_id,
        date=history_db.date,
        alert_type=history_db.alert_type,
        description=history_db.description,
    )


async def extract_dates_recharge(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_recharge = (
        await session.scalars(
            select(RefillHistory)
            .where(RefillHistory.printer_id == printer_id)
            .order_by(RefillHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_recharge:
        return [recharge.date for recharge in history_recharge]
    else:
        return []


async def extract_trash_dates(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_trash = (
        await session.scalars(
            select(PrinterTrashHistory)
            .where(PrinterTrashHistory.printer_id == printer_id)
            .order_by(PrinterTrashHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_trash:
        return [trash.date for trash in history_trash]
    else:
        return []


def _positive_intervals(dates: list[date]) -> tuple[list[date], list[int]]:
    """Remove duplicates, sort ascending, return (sorted_dates, positive_intervals_in_days)."""
    unique = sorted(set(dates))
    intervals = [
        (unique[i + 1] - unique[i]).days
        for i in range(len(unique) - 1)
        if (unique[i + 1] - unique[i]).days > 0
    ]
    return unique, intervals


def calculate_next_recharge(datas_recarga: list[date], type: str = "media") -> date | None:
    """
    Calcula a próxima data de recarga com base nas datas de recarga anteriores.
    Args:
        datas_recarga (list): Lista de datas de recarga.
        type (str): Tipo de cálculo a ser realizado. Pode ser "media" ou "mediana".
    Returns:
        date | None: A próxima data de recarga como objeto date, ou None se dados insuficientes.
    """
    datas, intervalos = _positive_intervals(datas_recarga)
    if not intervalos:
        return None
    if type == "media":
        dias = mean(intervalos)
    elif type == "mediana":
        dias = median(intervalos)
    else:
        raise ValueError(f"type deve ser 'media' ou 'mediana', recebido: {type!r}")
    return datas[-1] + timedelta(days=int(dias))


def calculate_recharge_percentage(datas_recarga: list[date], today: date | None = None) -> float:
    """
    Calcula o percentual de carga atual da impressora baseado no tempo decorrido
    desde a última recarga em relação à média de duração entre recargas.

    Args:
        datas_recarga (list): Lista de datas de recarga.
        today (date | None): Data de referência (default: date.today()).
    Returns:
        float: Percentual de carga atual (0-100).
               100% = recém recarregada (dia 0)
               50% = metade da vida útil
               0% = precisa recarga urgente
    """
    datas, intervalos = _positive_intervals(datas_recarga)
    if not intervalos:
        return 0.0

    if today is None:
        today = date.today()

    intervalo_medio_dias = mean(intervalos)
    dias_desde_ultima = (today - datas[-1]).days
    # Calcula o percentual de carga restante:
    # 100% = acabou de recarregar (0 dias)
    # 0% = tempo médio completo ou mais (precisa recarga)
    if intervalo_medio_dias > 0:
        tempo_passado_pct = (dias_desde_ultima / intervalo_medio_dias) * 100
        carga_restante_pct = 100 - tempo_passado_pct
        carga_restante_pct = max(0.0, min(100.0, carga_restante_pct))
        return round(carga_restante_pct, 2)
    return 0.0


def calculate_trash_cleaning_next_time(trash_datas: list[date]) -> date | None:
    """
    Calcula a próxima data de limpeza da lixeira com base no histórico de limpezas.
    Args:
        trash_datas (list): Lista de datas de limpeza da lixeira.
    Returns:
        date | None: A próxima data de limpeza como objeto date ou None se não houver dados suficientes.
    """
    datas, intervals = _positive_intervals(trash_datas)
    if not intervals:
        return None

    tempo_medio = sum(intervals) / len(intervals)
    return datas[-1] + timedelta(days=int(tempo_medio))


def calculate_trash_cleaning_percentage(trash_datas: list[date], today: date | None = None) -> float:
    """
    Calcula o percentual de limpeza da lixeira com base no histórico de limpezas.
    Args:
        trash_datas (list): Lista de datas de limpeza da lixeira.
        today (date | None): Data de referência (default: date.today()).
    Returns:
        float: O percentual de limpeza da lixeira (0.0-100.0).
    """
    datas, intervals = _positive_intervals(trash_datas)
    if not intervals:
        return 0.0

    if today is None:
        today = date.today()

    intervalo_medio_dias = mean(intervals)
    dias_desde_ultima = (today - datas[-1]).days

    # Calcula o percentual de limpeza necessária:
    # 0% = acabou de limpar (dia 0)
    # 100% = tempo médio completo ou mais (precisa limpeza urgente)
    if intervalo_medio_dias > 0:
        tempo_passado_pct = (dias_desde_ultima / intervalo_medio_dias) * 100
        necessidade_limpeza_pct = min(100.0, max(0.0, tempo_passado_pct))
        return round(necessidade_limpeza_pct, 2)
    return 0.0
