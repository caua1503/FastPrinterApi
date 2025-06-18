import os
import sys
from datetime import date

from sqlalchemy import select
import pytest

from app.models import Printer

@pytest.mark.asyncio
async def test_create_printer_db(session):
    printer = Printer(
        name="teste",
        model="teste",
        ip="192.168.1.1",
        brand="teste",
        department_id=1,
        status_id=1,
        supply_id=1,
        description="teste",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )

    session.add(printer)
    await session.commit()
    result = await session.scalar(select(Printer).where(Printer.ip == "192.168.1.1"))

    assert result.ip == "192.168.1.1"
