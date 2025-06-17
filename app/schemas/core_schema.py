from datetime import date

from pydantic import BaseModel


class InfoPrinterAll(BaseModel):
    id: int
    next_recharge: date
    percentage: float
    trash_cleaning_next_time: date
    trash_cleaning_percentage: float
