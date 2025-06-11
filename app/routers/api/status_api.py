from http import HTTPStatus
from fastapi import APIRouter
from models.status_model import StatusSchema

status_router = APIRouter(prefix="/status", tags=["status"])

@status_router.post("/", status_code=HTTPStatus.CREATED)
async def create_status(status: StatusSchema):
    ...

@status_router.put("/{id}")
async def update_status(id: int, status: StatusSchema):
    ...

@status_router.delete("/{id}")
async def delete_status(id: int):
    ...