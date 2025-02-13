from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.hash_pass import verify_password
from auth.jwt import create_access_token
from auth.roles import is_admin
from core import get_async_session
from models import User
from schemas.users_schemas import UserLogin


async def validate_user(
        user: UserLogin,
        db: AsyncSession = Depends(get_async_session),
        check_admin: bool = False
) -> str:
    """
    Validate user credentials.

    :param user: UserLogin Schema
    :param db: AsyncSession
    :param check_admin: Default False
    :return: JWT-token
    """
    db_user = await db.execute(select(User).where(User.username == user.username))
    user_data = db_user.scalar_one_or_none()

    if not user_data or not verify_password(user.password, user_data.hashed_password): # noqa
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not await is_admin(user_data.id, db) and check_admin: # noqa
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return create_access_token(data={"sub": user.username})
