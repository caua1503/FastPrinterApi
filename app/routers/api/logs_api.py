from fastapi import APIRouter, Depends, Query
from app.schemas.filter_schema import FilterLogUser, FilterLogSystem
from app.schemas.logs_schema import SystemLogSchema, UserLogSchema
from typing import List, Annotated

log_router = APIRouter()

@log_router.get("/system", response_model=List[SystemLogSchema])
async def api_get_system_log(filter: Annotated[FilterLogSystem, Query()]):
    return {"message": "Hello, World!"}

@log_router.get("/user", response_model=List[UserLogSchema])
async def api_get_user_log(filter: Annotated[FilterLogUser, Query()]):
    return {"message": "Hello, World!"}
