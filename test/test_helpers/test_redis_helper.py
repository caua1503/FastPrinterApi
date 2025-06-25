from datetime import date

import pytest

from app.helpers.redis_helper import (
    redis_get_value,
    redis_get_value_pydantic,
    redis_set_value,
    redis_set_value_pydantic,
)
from app.schemas.printer_schema import FullPrinterSchema, PrinterSchema


@pytest.mark.asyncio
async def test_set_and_get_value(session_redis):
    key = "test"
    value = "123"
    await redis_set_value(key, value, session_redis)
    result = await redis_get_value(key, session_redis)
    assert result == value


@pytest.mark.asyncio
async def test_set_and_get_value_pydantic(session_redis):
    key = "test"
    printer = FullPrinterSchema(
        name="Printer 1",
        description="Printer 1 description",
        status_id=1,
        supply_id=1,
        department_id=1,
        brand="Brand 1",
        model="Model 1",
        ip="192.168.1.1",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    await redis_set_value_pydantic(key, printer, session_redis)
    result = await redis_get_value_pydantic(key, FullPrinterSchema, redis_client=session_redis)
    assert result == printer


@pytest.mark.asyncio
async def test_set_and_get_list_value_pydantic(session_redis):
    key = "test"
    printer = PrinterSchema(
        name="Printer 1",
        model="Model 1",
        ip="192.168.1.1",
        brand="Brand 1",
    )
    list_pydantic = [printer, printer]
    await redis_set_value_pydantic(key, list_pydantic, session_redis)
    result = await redis_get_value_pydantic(key, PrinterSchema, True, session_redis)
    assert result == list_pydantic


@pytest.mark.asyncio
async def test_set_and_get_list_value_pydantic_with_date(session_redis):
    key = "test"
    printer = FullPrinterSchema(
        name="Printer 1",
        description="Printer 1 description",
        status_id=1,
        supply_id=1,
        department_id=1,
        brand="Brand 1",
        model="Model 1",
        ip="192.168.1.1",
        forecast=date.today(),
        last_refill=date.today(),
        last_maintenance=date.today(),
        last_check=date.today(),
    )
    list_pydantic = [printer, printer]
    await redis_set_value_pydantic(key, list_pydantic, session_redis)
    # result = await redis_get_value_pydantic(key, FullPrinterSchema, True, session_redis)
    # assert result == list_pydantic
