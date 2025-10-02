from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config import get_config
from app.helpers.core_helper import (
    calculate_next_recharge,
    calculate_recharge_percentage,
    calculate_trash_cleaning_next_time,
    calculate_trash_cleaning_percentage,
    create_history_alert_core,
    extract_dates_recharge,
    extract_trash_dates,
)
from app.models.history_model import MaintenanceInfoHistory
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer
from app.schemas.filter_schema import FilterBase
from app.schemas.history_schema import AlertHistorySchema

config = get_config()


async def get_all_printers_maintenance_info(session: AsyncSession, filters: FilterBase):
    """
    Atualiza as informações de manutenção para todas as impressoras.
    Processa todas as impressoras em uma única transação para manter atomicidade.

    Args:
        session (AsyncSession): Sessão do banco de dados.
        filters (FilterBase): Filtros para análise histórica.

    Returns:
        None: A função atualiza os dados no banco, não retorna valores.
    """
    try:
        batch_size = config.PRINTER_MAINTENANCE_BATCH_SIZE
        objects_to_add = []
        alert_cleaning_percentage = 10
        query = select(Printer)

        async for printer in await session.stream_scalars(query):
            datas_recarga = await extract_dates_recharge(printer.id, session, filters)
            trash_datas = await extract_trash_dates(printer.id, session, filters)

            if datas_recarga:
                next_recharge_date = calculate_next_recharge(datas_recarga, "media")
                percentage = calculate_recharge_percentage(datas_recarga)
            else:
                next_recharge_date = None
                percentage = 0.0

            trash_cleaning_next_time_date = calculate_trash_cleaning_next_time(trash_datas)
            trash_cleaning_percentage_value = calculate_trash_cleaning_percentage(trash_datas)

            if trash_cleaning_percentage_value <= alert_cleaning_percentage:
                alert_description = f"A limpeza da lixeira é urgente, percentual: {trash_cleaning_percentage_value}%"
                alert_history = AlertHistorySchema(
                    printer_id=printer.id,
                    date=date.today(),
                    alert_type="limpeza_urgente",
                    description=alert_description,
                )
                await create_history_alert_core(alert_history, session)

            exist_maintenance_info = await session.scalar(
                select(PrinterMaintenanceInfo).where(PrinterMaintenanceInfo.printer_id == printer.id)
            )

            history_recharge = MaintenanceInfoHistory(
                printer_id=printer.id,
                refill_percentage=percentage,
                cleaning_percentage=trash_cleaning_percentage_value,
            )
            objects_to_add.append(history_recharge)

            if exist_maintenance_info:
                exist_maintenance_info.next_refill = next_recharge_date
                exist_maintenance_info.refill_percentage = percentage
                exist_maintenance_info.cleaning_percentage = trash_cleaning_percentage_value
                exist_maintenance_info.next_cleaning = trash_cleaning_next_time_date
                exist_maintenance_info.last_update = date.today()
            else:
                new_maintenance_info = PrinterMaintenanceInfo(
                    printer_id=printer.id,
                    last_update=date.today(),
                    refill_percentage=percentage,
                    cleaning_percentage=trash_cleaning_percentage_value,
                    next_refill=next_recharge_date,
                    next_cleaning=trash_cleaning_next_time_date,
                )
                objects_to_add.append(new_maintenance_info)

            if len(objects_to_add) >= batch_size:
                session.add_all(objects_to_add)
                objects_to_add.clear()

        if objects_to_add:
            session.add_all(objects_to_add)

        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e


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
    datas_recarga = await extract_dates_recharge(printer_id, session, filters)
    trash_datas = await extract_trash_dates(printer_id, session, filters)

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
