from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.department_schema import DepartmentSchema
from app.schemas.filter_schema import FilterBase
from app.services.department_service import (
    create_department,
    delete_department,
    get_department_id,
    get_departments,
    update_department,
)

department_router = APIRouter()


@department_router.get("/", summary="Get all departments")
async def api_get_departments(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterBase, Query()],
    current_user=has_access(),
):
    departments = await get_departments(session, filters)
    return {"departments": departments}


@department_router.post("/", summary="Create a department")
async def api_create_department(
    department: DepartmentSchema, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    department_db = await create_department(session, department)
    return department_db


@department_router.get("/{id}", summary="Get a department by id")
async def api_get_department_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    department = await get_department_id(session, id)
    return department


@department_router.put("/{id}", summary="Update a department by id")
async def api_update_department(
    id: int,
    department: DepartmentSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    department_db = await update_department(session, id, department)
    return department_db


@department_router.delete("/{id}", summary="Delete a department by id")
async def api_delete_department(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    result = await delete_department(session, id)
    return result
