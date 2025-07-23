from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import (
    get_api_key,
    get_password_hash,
    verify_password,
)
from app.helpers.database_helper import get_redis_client
from app.helpers.redis_helper import (
    redis_get_value_pydantic,
    redis_set_value_pydantic,
)
from app.models.user_model import User, UserApiKey, UserConfiguration
from app.schemas.user_schema import (
    UserApiKeySchema,
    UserCreateAdminSchema,
    UserCreateSchema,
    UserNewPasswordAdminSchema,
    UserNewPasswordSchema,
    UsersRoleSchema,
    UserUpdateAdminSchema,
    UserUpdateSchema,
)


async def create_user(session: AsyncSession, user: UserCreateSchema | UserCreateAdminSchema):
    existing_user = await session.scalar(select(User).where(User.login == user.login))

    if existing_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Usuário já existe")

    user_db = User(
        login=user.login,
        password_hash=get_password_hash(password=user.password),
        name=user.name,
        role=user.role if isinstance(user, UserCreateAdminSchema) else UsersRoleSchema.guest,
    )

    session.add(user_db)
    await session.flush()

    user_configuration = UserConfiguration(
        user_id=user_db.id,
        username=user.name,
    )

    session.add(user_configuration)
    await session.commit()
    await session.refresh(user_db)

    return user_db


async def update_user(session: AsyncSession, id: int, user: UserUpdateSchema | UserUpdateAdminSchema):
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

    if isinstance(user, UserUpdateAdminSchema) and user.role:
        existing_user.role = user.role

    await session.commit()
    await session.refresh(existing_user)
    return existing_user


async def update_user_password(session: AsyncSession, id: int, user_password: UserNewPasswordSchema):
    existing_user = await session.scalar(select(User).where(User.id == id))

    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    if not verify_password(user_password.current_password, existing_user.password_hash):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Current password is incorrect ")

    existing_user.password_hash = get_password_hash(user_password.new_password)

    await session.commit()
    await session.refresh(existing_user)


async def update_user_password_admin(session: AsyncSession, id: int, user_password: UserNewPasswordAdminSchema):
    existing_user = await session.scalar(select(User).where(User.id == id))

    if not existing_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    existing_user.password_hash = get_password_hash(user_password.new_password)

    await session.commit()
    await session.refresh(existing_user)


async def create_api_key(session: AsyncSession, id: int):
    new_api_key = await get_api_key(session)

    user_api_key = UserApiKey(
        user_id=id,
        api_key=new_api_key,
    )

    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)

    return user_api_key


async def get_api_key_from_user_id(session: AsyncSession, id: int):
    user_api_key = (await session.scalars(select(UserApiKey).where(UserApiKey.user_id == id))).all()

    if not user_api_key:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="API key não encontrada")
    redis_client = await get_redis_client()
    list_api_key = await redis_get_value_pydantic(
        f"list_api_key_{id}", UserApiKeySchema, is_list=True, redis_client=redis_client
    )

    if list_api_key:
        return list_api_key

    list_api_key = [UserApiKeySchema(api_key=api_key.api_key) for api_key in user_api_key]

    if list_api_key:
        await redis_set_value_pydantic(f"list_api_key_{id}", list_api_key)

    return list_api_key if list_api_key else []


async def delete_user(session: AsyncSession, id: int):
    user = await session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    await session.delete(user)
    await session.commit()


async def update_first_access(session: AsyncSession, id: int):
    user = await session.scalar(select(User).options(selectinload(User.configuration)).where(User.id == id))

    if user.configuration.first_access:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User already has first registered access")

    user.configuration.first_access = True
    await session.commit()
    await session.refresh(user.configuration)
