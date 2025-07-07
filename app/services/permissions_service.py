from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import ApiKeyPermission, PermissionApiKey, PermissionUser, UserPermission
from app.schemas.permission_schema import (
    ListPermissionApiKeySchema,
    ListPermissionUserSchema,
    PermissionApiKeySchema,
    PermissionApiKeyUpdateSchema,
    PermissionUserSchema,
    PermissionUserUpdateSchema,
)


async def get_all_permissions_user(session: AsyncSession):
    query = select(PermissionUser)
    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        return ListPermissionUserSchema(total=0, permissions=[])

    result = (await session.scalars(query)).all()

    return ListPermissionUserSchema(
        total=total,
        permissions=result,  # type: ignore
    )


async def get_all_permissions_api_key(session: AsyncSession):
    query = select(PermissionApiKey)
    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        return ListPermissionApiKeySchema(total=0, permissions=[])

    result = (await session.scalars(query)).all()

    return ListPermissionApiKeySchema(
        total=total,
        permissions=result,  # type: ignore
    )


async def create_permission_user(permission: PermissionUserSchema, session: AsyncSession):
    result = await session.scalar(select(PermissionUser).where(PermissionUser.code == permission.code))

    if result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission already exists")

    db_permission = PermissionUser(
        name=permission.name,
        code=permission.code,
        description=permission.description,
    )

    session.add(db_permission)
    await session.commit()
    await session.refresh(db_permission)

    return db_permission


async def create_permission_api_key(permission: PermissionApiKeySchema, session: AsyncSession):
    result = await session.scalar(select(PermissionApiKey).where(PermissionApiKey.code == permission.code))

    if result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission already exists")

    db_permission = PermissionApiKey(
        name=permission.name,
        code=permission.code,
        description=permission.description,
    )

    session.add(db_permission)
    await session.commit()
    await session.refresh(db_permission)

    return db_permission


async def update_permission_user(permission_id: int, permission: PermissionUserUpdateSchema, session: AsyncSession):
    result = await session.scalar(select(PermissionUser).where(PermissionUser.id == permission_id))

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission not found")

    result.name = permission.name if permission.name else result.name
    result.description = permission.description if permission.description else result.description

    await session.commit()
    await session.refresh(result)

    return result


async def update_permission_api_key(
    permission_id: int,
    permission: PermissionApiKeyUpdateSchema,
    session: AsyncSession,
):
    result = await session.scalar(select(PermissionApiKey).where(PermissionApiKey.id == permission_id))

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission not found")

    result.name = permission.name if permission.name else result.name
    result.description = permission.description if permission.description else result.description

    await session.commit()
    await session.refresh(result)

    return result


async def delete_permission_user(permission_id: int, session: AsyncSession):
    result = await session.scalar(select(PermissionUser).where(PermissionUser.id == permission_id))

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission not found")

    users = (await session.scalars(select(UserPermission).where(UserPermission.permission_id == permission_id))).all()

    if users:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Permission is in use by {len(users)} users")

    await session.delete(result)
    await session.commit()

    return result


async def delete_permission_api_key(permission_id: int, session: AsyncSession):
    result = await session.scalar(select(PermissionApiKey).where(PermissionApiKey.id == permission_id))

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Permission not found")

    api_keys = (
        await session.scalars(select(ApiKeyPermission).where(ApiKeyPermission.permission_id == permission_id))
    ).all()

    if api_keys:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Permission is in use by {len(api_keys)} api keys"
        )

    await session.delete(result)
    await session.commit()

    return result
