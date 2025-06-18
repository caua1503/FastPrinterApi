from http import HTTPStatus

from core.security import generate_random_code, get_password_hash
from fastapi import HTTPException
from models.user_model import User
from schemas.user_schema import UserSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, user: UserSchema):
    existing_user = await session.scalar(select(User).where(User.login == user.login))

    if existing_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Usuário já existe")

    user_db = User(login=user.login, password_hash=get_password_hash(user.password), name=user.name, email=user.email)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def update_user(session: AsyncSession, id: int, user: UserSchema):
    existing_user = await session.scalar(select(User).where(User.id == id))
    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    existing_user_login = await session.scalar(select(User).where(User.login == user.login))
    if existing_user_login:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Login já existe")

    existing_user.login = user.login
    existing_user.name = user.name

    await session.commit()
    await session.refresh(existing_user)
    return existing_user


async def update_user_password(session: AsyncSession, id: int, password: str):
    existing_user = await session.scalar(select(User).where(User.id == id))
    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    code_hash = generate_random_code(8)
    existing_user.password_hash = get_password_hash(password, code_hash)
    existing_user.code_hash = code_hash
    await session.commit()
    await session.refresh(existing_user)


async def delete_user(session: AsyncSession, id: int):
    user = await session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    await session.delete(user)
    await session.commit()
    return user
