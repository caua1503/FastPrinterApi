from datetime import date, datetime, timedelta
from statistics import mean, median

from models.model_db import Historico_Recarga, Impressora
from sqlalchemy import select
from sqlalchemy.orm import Session


def _get_printers(session: Session):
    printers_database = session.scalars(select(Impressora)).all()
    print(printers_database)
    return printers_database


def _extract_datas_recarga(printer_id: int, session: Session) -> list[str]:
    history_recharge = session.scalars(
        select(Historico_Recarga).where(Historico_Recarga.impressora_id == printer_id)
    ).all()
    if history_recharge:
        return [recharge.data for recharge in history_recharge]
    else:
        return []


def get_all_printers_recarga_datas(session: Session) -> dict:
    """
    Retorna um dicionário com o id da impressora como chave e a lista de datas de recarga como valor.
    """
    result = {printer.id: _extract_datas_recarga(printer.id, session) for printer in _get_printers(session)}

    return [{printer_id: _calculate_next_recharge(datas, "media")} for printer_id, datas in result.items()]


def _calculate_next_recharge(datas_recarga: list, type: str = "media") -> str:
    # Garante que todos os elementos sejam datetime
    datas = [
        data if isinstance(data, (datetime, date)) else datetime.strptime(data, "%d/%m/%Y") for data in datas_recarga
    ]
    data_ultima_recarga = datas[-1]
    intervalos = [(datas[i + 1] - datas[i]).days for i in range(len(datas) - 1)]
    if type == "media":
        dias = mean(intervalos)
    elif type == "mediana":
        dias = median(intervalos)
    return (data_ultima_recarga + timedelta(days=int(dias))).strftime("%d/%m/%Y")


def send_message_webhook(message: str, webhook_url: str) -> None: ...
