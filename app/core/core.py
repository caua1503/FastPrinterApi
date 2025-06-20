from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.filters import FilterBase
from app.helpers.core_helper import (
    calculate_next_recharge,
    calculate_recharge_percentage,
    calculate_trash_cleaning_next_time,
    calculate_trash_cleaning_percentage,
    extract_datas_recharge,
    extract_trash_datas,
    get_printers,
)
from app.models.history_model import AlertHistory


async def get_all_printers_maintenance_info(session: AsyncSession, filters: FilterBase):
    """
    Retorna uma lista de dicionários com o id da impressora, a próxima data de recarga, o percentual de carga atual,
    a próxima data de limpeza da lixeira e o percentual de necessidade de limpeza da lixeira.
    Args:
        session (Session): Sessão do banco de dados.
        limit (int): Limite de registros históricos para análise.
    Returns:
        List[dict]: Lista de dicionários com:
            - id (int): ID da impressora
            - next_recharge (str): Próxima data de recarga formatada como dd/mm/yyyy
            - percentage (float): Percentual de carga atual
            - trash_cleaning_next_time (str): Próxima data de limpeza da lixeira formatada como dd/mm/yyyy
            - trash_cleaning_percentage (float): Percentual de necessidade de limpeza da lixeira (0.0-100.0)
    """
    printers = await get_printers(session)
    result = []

    for printer in printers:
        datas_recarga = await extract_datas_recharge(printer.id, session, filters)
        trash_datas = await extract_trash_datas(printer.id, session, filters)

        if datas_recarga:
            next_recharge_date = calculate_next_recharge(datas_recarga, "media")
            next_recharge = next_recharge_date.strftime("%d/%m/%Y")
            percentage = calculate_recharge_percentage(datas_recarga)
        else:
            next_recharge = "N/A"
            percentage = 0.0

        trash_cleaning_next_time_date = calculate_trash_cleaning_next_time(trash_datas)
        trash_cleaning_next_time = (
            trash_cleaning_next_time_date.strftime("%d/%m/%Y") if trash_cleaning_next_time_date else "N/A"
        )
        trash_cleaning_percentage_value = calculate_trash_cleaning_percentage(trash_datas)

        alert_cleaning_percentage = 10

        if trash_cleaning_percentage_value <= alert_cleaning_percentage:
            # Import dinâmico para evitar circular import
            from app.services.history_service import create_history_alert  # noqa: PLC0415

            alert_description = f"A limpeza da lixeira é urgente, percentual: {trash_cleaning_percentage_value}%"
            alert_history = AlertHistory(
                printer_id=printer.id,
                date=datetime.now(),
                alert_type="limpeza_urgente",
                description=alert_description,
            )
            await create_history_alert(alert_history, session)

        result.append({
            "id": printer.id,
            "next_recharge": next_recharge,
            "percentage": percentage,
            "trash_cleaning_next_time": trash_cleaning_next_time,
            "trash_cleaning_percentage": trash_cleaning_percentage_value,
        })

    return result


async def get_printer_maintenance_info(printer_id: int, session: AsyncSession, filters: FilterBase):
    """
    Retorna um dicionário com as informações de manutenção da impressora.
    Args:
        printer_id (int): ID da impressora.
        session (AsyncSession): Sessão do banco de dados.
        limit (int): Limite de registros históricos para análise.
    Returns:
        dict: Dicionário com:
            - id (int): ID da impressora
            - next_recharge (date | None): Próxima data de recarga como objeto date ou None
            - percentage (float): Percentual de carga atual (0.0-100.0)
            - trash_cleaning_next_time (date | None): Próxima data de limpeza da lixeira como objeto date ou None
            - trash_cleaning_percentage (float): Percentual de necessidade de limpeza da lixeira (0.0-100.0)
    """
    datas_recarga = await extract_datas_recharge(printer_id, session, filters)
    trash_datas = await extract_trash_datas(printer_id, session, filters)

    if datas_recarga:
        next_recharge_date = calculate_next_recharge(datas_recarga, "media")
        percentage = calculate_recharge_percentage(datas_recarga)
    else:
        next_recharge_date = None
        percentage = 0.0

    trash_cleaning_next_time_date = calculate_trash_cleaning_next_time(trash_datas)
    trash_cleaning_percentage_value = calculate_trash_cleaning_percentage(trash_datas)

    return {
        "id": printer_id,
        "next_recharge": next_recharge_date,
        "percentage": percentage,
        "trash_cleaning_next_time": trash_cleaning_next_time_date,
        "trash_cleaning_percentage": trash_cleaning_percentage_value,
    }


async def send_message_webhook(message: str, webhook_url: str) -> None: ...
