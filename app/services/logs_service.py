from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.logs_model import ApiKeyLog, SystemLog, UserLog
from app.schemas.filter_schema import FilterLogApiKey, FilterLogSystem, FilterLogUser, OrderBy, OrderByFieldLog
from app.schemas.logs_schema import ListApiKeyLogSchema, ListSystemLogSchema, ListUserLogSchema


async def get_user_logs(session: AsyncSession, filters: FilterLogUser):
    query = select(UserLog)
    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        return ListUserLogSchema(total=0, count=0, logs=[])

    if filters.service:
        query = query.filter(UserLog.service == filters.service)
    if filters.level:
        query = query.filter(UserLog.level == filters.level)
    if filters.time_start:
        query = query.filter(UserLog.timestamp >= filters.time_start)
    if filters.time_end:
        query = query.filter(UserLog.timestamp <= filters.time_end)
    if filters.user_id:
        query = query.filter(UserLog.user_id == filters.user_id)

    if filters.order_by_field:
        order_by_mapping = {
            OrderByFieldLog.created_at: UserLog.created_at,
            OrderByFieldLog.timestamp: UserLog.timestamp,
        }
        column = order_by_mapping[filters.order_by_field]
        query = query.order_by(column.desc() if filters.order_by == OrderBy.desc else column.asc())
    else:
        query = query.order_by(
            UserLog.timestamp.desc() if filters.order_by == OrderBy.desc else UserLog.timestamp.asc()
        )

    query = query.limit(filters.limit).offset(filters.offset)

    result = (await session.scalars(query)).all()

    return ListUserLogSchema(total=total, count=len(result), logs=result)  # type: ignore


async def get_system_logs(session: AsyncSession, filters: FilterLogSystem):
    query = select(SystemLog)
    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        ListSystemLogSchema(total=0, count=0, logs=[])

    if filters.service:
        query = query.filter(SystemLog.service == filters.service)
    if filters.level:
        query = query.filter(SystemLog.level == filters.level)
    if filters.time_start:
        query = query.filter(SystemLog.timestamp >= filters.time_start)
    if filters.time_end:
        query = query.filter(SystemLog.timestamp <= filters.time_end)

    if filters.order_by_field:
        order_by_mapping = {
            OrderByFieldLog.created_at: SystemLog.created_at,
            OrderByFieldLog.timestamp: SystemLog.timestamp,
        }
        column = order_by_mapping[filters.order_by_field]
        query = query.order_by(column.desc() if filters.order_by == OrderBy.desc else column.asc())
    else:
        query = query.order_by(
            SystemLog.timestamp.desc() if filters.order_by == OrderBy.desc else SystemLog.timestamp.asc()
        )

    query = query.limit(filters.limit).offset(filters.offset)

    result = (await session.scalars(query)).all()

    return ListSystemLogSchema(total=total, count=len(result), logs=result)  # type: ignore


async def get_api_key_logs(session: AsyncSession, filters: FilterLogApiKey, user_id: Optional[int] = None):
    query = select(ApiKeyLog)

    if user_id:
        query = query.filter(ApiKeyLog.user_id == user_id)

    user_ids: Optional[List[int]] = getattr(filters, "user_ids", None)

    if user_ids:
        query = query.filter(ApiKeyLog.user_id.in_(user_ids))

    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        return ListApiKeyLogSchema(total=0, count=0, logs=[])

    if filters.action:
        query = query.filter(ApiKeyLog.action == filters.action)
    if filters.api_key_id:
        query = query.filter(ApiKeyLog.api_key_id == filters.api_key_id)
    if filters.time_start:
        query = query.filter(ApiKeyLog.timestamp >= filters.time_start)
    if filters.time_end:
        query = query.filter(ApiKeyLog.timestamp <= filters.time_end)

    if filters.order_by_field:
        order_by_mapping = {
            OrderByFieldLog.created_at: ApiKeyLog.created_at,
            OrderByFieldLog.timestamp: ApiKeyLog.timestamp,
        }
        column = order_by_mapping[filters.order_by_field]
        query = query.order_by(column.desc() if filters.order_by == OrderBy.desc else column.asc())
    else:
        query = query.order_by(
            ApiKeyLog.timestamp.desc() if filters.order_by == OrderBy.desc else ApiKeyLog.timestamp.asc()
        )

    query = query.limit(filters.limit).offset(filters.offset)

    result = (await session.scalars(query)).all()

    return ListApiKeyLogSchema(total=total, count=len(result), logs=result)  # type: ignore
