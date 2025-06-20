from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department_model import Department
from app.models.printer_model import Printer
from app.schemas.department_schema import DepartmentSchema
from app.schemas.filters import FilterBase


async def create_department(session: AsyncSession, department: DepartmentSchema):
    existing_department = await session.scalar(select(Department).where(Department.name == department.name))

    if existing_department:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Department already exists")

    department_db = Department(name=department.name, description=department.description)

    session.add(department_db)
    await session.commit()
    await session.refresh(department_db)

    return department_db


async def get_departments(session: AsyncSession, filters: FilterBase):
    departments = (await session.scalars(select(Department).limit(filters.limit).offset(filters.offset))).all()
    return departments


async def get_department_id(session: AsyncSession, id: int):
    department = await session.scalar(select(Department).where(Department.id == id))
    if not department:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found")
    return department


async def update_department(session: AsyncSession, id: int, department: DepartmentSchema):
    existing_department = await session.scalar(select(Department).where(Department.id == id))
    if not existing_department:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found")

    existing_department.name = department.name
    existing_department.description = department.description

    await session.commit()
    await session.refresh(existing_department)
    return existing_department


async def delete_department(session: AsyncSession, id: int):
    department = await session.scalar(select(Department).where(Department.id == id))
    printers = await session.scalars(select(Printer).where(Printer.department_id == id))

    if not department:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found")

    if printers:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Department has printers")

    await session.delete(department)
    await session.commit()
    return department
