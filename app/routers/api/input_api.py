from http import HTTPStatus
from fastapi import APIRouter
from models.input_model import InputSchema

input_router = APIRouter(prefix="/input", tags=["input"])

@input_router.post("/", status_code=HTTPStatus.CREATED)
async def create_input(input: InputSchema):
    ...

@input_router.put("/{id}")
async def update_input(id: int, input: InputSchema):
    ...
@input_router.delete("/{id}")
async def delete_input(id: int):
    ...