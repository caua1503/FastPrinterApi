from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.database_helper import get_session
from app.schemas.department_schema import DepartmentSchema
from app.services.department_service import (
    create_department,
    delete_department,
    get_department_id,
    get_departments,
    update_department,
)

department_router = APIRouter()


@department_router.get("/", description="Get all departments")
async def api_get_departments(session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0):
    departments = await get_departments(session, limit, offset)
    return {"departments": departments}


@department_router.post("/", description="Create a department")
async def api_create_department(department: DepartmentSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    department_db = await create_department(session, department)
    return department_db


@department_router.get("/{id}", description="Get a department by id")
async def api_get_department_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    department = await get_department_id(session, id)
    return department


@department_router.put("/{id}", description="Update a department by id")
async def api_update_department(
    id: int, department: DepartmentSchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    department_db = await update_department(session, id, department)
    return department_db


@department_router.delete("/{id}", description="Delete a department by id")
async def api_delete_department(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await delete_department(session, id)
    return result
