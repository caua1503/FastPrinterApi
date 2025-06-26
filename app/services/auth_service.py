from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.models.user_model import User
from app.schemas.token_schema import TokenSchema


async def get_token_jwt(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    user = await session.scalar(select(User).where(User.login == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invalid credencials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invalid credencials")    

    data = {
        "sub": str(user.id),
    }

    token = TokenSchema(
        access_token=create_access_token(data),
        token_type="bearer",
    )

    return token
