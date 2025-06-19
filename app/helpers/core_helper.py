from datetime import date, datetime, timedelta
from statistics import mean, median
from typing import List

from app.models.history_model import PrinterTrashHistory, RefillHistory
from app.models.printer_model import Printer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_printers(session: AsyncSession):
    printers_database = (await session.scalars(select(Printer))).all()
    return printers_database


async def extract_datas_recharge(printer_id: int, session: AsyncSession, limit: int) -> List:
    history_recharge = (
        await session.scalars(
            select(RefillHistory)
            .where(RefillHistory.printer_id == printer_id)
            .order_by(RefillHistory.date.desc())
            .limit(limit)
        )
    ).all()
    if history_recharge:
        return [recharge.data for recharge in history_recharge]
    else:
        return []


async def extract_trash_datas(printer_id: int, session: AsyncSession, limit: int) -> List:
    history_trash = (
        await session.scalars(
            select(PrinterTrashHistory)
            .where(PrinterTrashHistory.printer_id == printer_id)
            .order_by(PrinterTrashHistory.date.desc())
            .limit(limit)
        )
    ).all()
    if history_trash:
        return [trash.data for trash in history_trash]
    else:
        return []


def calculate_next_recharge(datas_recarga: list, type: str = "media") -> date:
    """
    Calcula a próxima data de recarga com base nas datas de recarga anteriores.
    Args:
        datas_recarga (list): Lista de datas de recarga.
        type (str): Tipo de cálculo a ser realizado. Pode ser "media" ou "mediana".
    Returns:
        date: A próxima data de recarga como objeto date.
    """
    datas = []
    for data in datas_recarga:
        if isinstance(data, (datetime, date)):
            if isinstance(data, date) and not isinstance(data, datetime):
                datas.append(datetime.combine(data, datetime.min.time()))
            else:
                datas.append(data)
        else:
            datas.append(datetime.strptime(data, "%d/%m/%Y"))

    data_ultima_recarga = datas[-1]
    intervalos = [(datas[i + 1] - datas[i]).days for i in range(len(datas) - 1)]
    if type == "media":
        dias = mean(intervalos)
    elif type == "mediana":
        dias = median(intervalos)
    resultado = data_ultima_recarga + timedelta(days=int(dias))
    return resultado.date()


def calculate_recharge_percentage(datas_recarga: list) -> float:
    """
    Calcula o percentual de carga atual da impressora baseado no tempo decorrido
    desde a última recarga em relação à média de duração entre recargas.

    Args:
        datas_recarga (list): Lista de datas de recarga.
    Returns:
        float: Percentual de carga atual (0-100).
               100% = recém recarregada (dia 0)
               50% = metade da vida útil
               0% = precisa recarga urgente
    """
    datas_minima = 2
    if len(datas_recarga) < datas_minima:
        return 0.0

    datas = []
    for data in datas_recarga:
        if isinstance(data, (datetime, date)):
            if isinstance(data, date) and not isinstance(data, datetime):
                datas.append(datetime.combine(data, datetime.min.time()))
            else:
                datas.append(data)
        else:
            datas.append(datetime.strptime(data, "%d/%m/%Y"))

    datas.sort()

    intervalos = [(datas[i + 1] - datas[i]).days for i in range(len(datas) - 1)]
    intervalo_medio_dias = mean(intervalos)
    data_ultima_recarga = datas[-1]
    hoje = datetime.now()
    dias_desde_ultima = (hoje - data_ultima_recarga).days
    # Calcula o percentual de carga restante:
    # 100% = acabou de recarregar (0 dias)
    # 0% = tempo médio completo ou mais (precisa recarga)
    if intervalo_medio_dias > 0:
        tempo_passado_pct = (dias_desde_ultima / intervalo_medio_dias) * 100
        carga_restante_pct = 100 - tempo_passado_pct
        carga_restante_pct = max(0.0, min(100.0, carga_restante_pct))
        return round(carga_restante_pct, 2)
    return 0.0


def calculate_trash_cleaning_next_time(trash_datas: list) -> date | None:
    """
    Calcula a próxima data de limpeza da lixeira com base no histórico de limpezas.
    Args:
        trash_datas (list): Lista de datas de limpeza da lixeira.
    Returns:
        date | None: A próxima data de limpeza como objeto date ou None se não houver dados suficientes.
    """
    datas_minima = 2
    if len(trash_datas) < datas_minima:
        return None

    datas = []
    for data in trash_datas:
        if isinstance(data, (datetime, date)):
            if isinstance(data, date) and not isinstance(data, datetime):
                datas.append(datetime.combine(data, datetime.min.time()))
            else:
                datas.append(data)
        else:
            datas.append(datetime.strptime(data, "%d/%m/%Y"))

    datas.sort(reverse=True)

    intervals = [(datas[i] - datas[i + 1]).days for i in range(len(datas) - 1) if (datas[i] - datas[i + 1]).days > 0]

    if not intervals:
        return None

    tempo_medio = sum(intervals) / len(intervals)
    ultima_limpeza = datas[0]
    proxima_prevista = ultima_limpeza + timedelta(days=int(tempo_medio))

    return proxima_prevista.date()


def calculate_trash_cleaning_percentage(trash_datas: list) -> float:
    """
    Calcula o percentual de limpeza da lixeira com base no histórico de limpezas.
    Args:
        trash_datas (list): Lista de datas de limpeza da lixeira.
    Returns:
        float: O percentual de limpeza da lixeira (0.0-100.0).
    """
    datas_minima = 2
    if len(trash_datas) < datas_minima:
        return 0.0

    datas = []
    for data in trash_datas:
        if isinstance(data, (datetime, date)):
            if isinstance(data, date) and not isinstance(data, datetime):
                datas.append(datetime.combine(data, datetime.min.time()))
            else:
                datas.append(data)
        else:
            datas.append(datetime.strptime(data, "%d/%m/%Y"))

    datas.sort(reverse=True)

    intervals = [(datas[i] - datas[i + 1]).days for i in range(len(datas) - 1) if (datas[i] - datas[i + 1]).days > 0]

    if not intervals:
        return 0.0

    intervalo_medio_dias = mean(intervals)
    ultima_limpeza = datas[0]
    hoje = datetime.now()
    dias_desde_ultima = (hoje - ultima_limpeza).days

    # Calcula o percentual de limpeza necessária:
    # 0% = acabou de limpar (dia 0)
    # 100% = tempo médio completo ou mais (precisa limpeza urgente)
    if intervalo_medio_dias > 0:
        tempo_passado_pct = (dias_desde_ultima / intervalo_medio_dias) * 100
        necessidade_limpeza_pct = min(100.0, max(0.0, tempo_passado_pct))
        return round(necessidade_limpeza_pct, 2)
    return 0.0
