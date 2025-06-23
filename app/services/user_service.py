from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    get_api_key,
    get_password_hash,
)
from app.models.user_model import User, UserApiKey
from app.schemas.user_schema import UserCreateSchema, UserPasswordSchema, UserUpdateSchema


async def create_user(session: AsyncSession, user: UserCreateSchema):
    existing_user = await session.scalar(select(User).where(User.login == user.login))

    if existing_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Usuário já existe")

    user_db = User(
        login=user.login,
        password_hash=get_password_hash(password=user.password),
        name=user.name,
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def update_user(session: AsyncSession, id: int, user: UserUpdateSchema):
    existing_user = await session.scalar(select(User).where(User.id == id))
    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    if user.login:
        existing_user_login = await session.scalar(select(User).where(User.login == user.login))
        if existing_user_login and existing_user_login.id != id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Login já existe")
        existing_user.login = user.login

    if user.name:
        existing_user.name = user.name

    await session.commit()
    await session.refresh(existing_user)
    return existing_user


async def update_user_password(session: AsyncSession, id: int, password: UserPasswordSchema):
    existing_user = await session.scalar(select(User).where(User.id == id))
    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    existing_user.password_hash = get_password_hash(password.password)
    await session.commit()
    await session.refresh(existing_user)


async def create_api_key(session: AsyncSession, id: int):
    # user = await session.scalar(select(User).where(User.id == id))

    new_api_key = await get_api_key(session)

    user_api_key = UserApiKey(
        user_id=id,
        api_key=new_api_key,
    )

    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)

    return user_api_key


async def delete_user(session: AsyncSession, id: int):
    user = await session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    await session.delete(user)
    await session.commit()
