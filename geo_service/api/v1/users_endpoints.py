import logging

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.validators import validate_user
from auth.hash_pass import hash_password, verify_password
from auth.users import get_current_user
from core import get_async_session
from models import User, Role
from schemas.users_schemas import UserRegister, Token, UserLogin, UserProfile, ChangePassword

router = APIRouter(prefix='/users')

logger = logging.getLogger(__name__)

@router.post("/register", response_model=dict)
async def register_user(user: UserRegister, db: AsyncSession = Depends(get_async_session)):
    """
    Registration user.
    """
    existing_user = await db.execute(User.__table__.select().where(User.username == user.username))

    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    user_role = await db.execute(select(Role).where(Role.name == "user"))
    role = user_role.scalar_one_or_none()

    if role:
        new_user.role_id = role.id

    db.add(new_user)
    await db.commit()

    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    """
    Authorization user.
    """
    logger.info(f"Login user: {user}")
    access_token = await validate_user(user, db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserProfile)
async def user_profile(user: User = Depends(get_current_user)):
    """
    Get user profile.
    """
    return {
        "username": user.username,
        "role": user.role
    }


@router.post("/change_password", response_model=dict)
async def change_password(
    data: ChangePassword,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Change user password.
    """
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")

    user.hashed_password = hash_password(data.new_password)
    await db.commit()

    return {"message": "Password updated successfully"}