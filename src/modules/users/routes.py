from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.common.dependencies import get_db
from src.modules.users import schemas, services, auth
from src.modules.users.dependencies import get_current_user
from src.modules.users.models import User


router = APIRouter(prefix="/users", tags=["Users"])

# 📌 Создать нового пользователя
@router.post(
    "/", 
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Register a new user account"
)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await services.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return await services.create_user(db, user_in)


# 📌 Получить список пользователей
@router.get(
    "/", 
    response_model=list[schemas.UserOut],
    summary="Get users list",
    description="Retrieve list of users with pagination"
)
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await services.get_users(db, skip=skip, limit=limit)


# 📌 Получить пользователя по ID
@router.get(
    "/{user_id}", 
    response_model=schemas.UserOut,
    summary="Get user by ID",
    description="Retrieve specific user by their ID"
)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await services.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user


# 📌 Текущий пользователь (ДОБАВЛЕНО)
@router.get(
    "/me/", 
    response_model=schemas.UserOut,
    summary="Get current user",
    description="Retrieve authenticated user's profile"
)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


# 📌 Обновить текущего пользователя (ДОБАВЛЕНО)
@router.put(
    "/me/", 
    response_model=schemas.UserOut,
    summary="Update current user",
    description="Update authenticated user's profile"
)
async def update_current_user(
    user_in: schemas.UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    db_user = await services.update_user(db, current_user.id, user_in)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


# 📌 Обновить пользователя по ID
@router.put(
    "/{user_id}", 
    response_model=schemas.UserOut,
    summary="Update user by ID",
    description="Update specific user by their ID"
)
async def update_user(
    user_id: int, 
    user_in: schemas.UserUpdate, 
    db: AsyncSession = Depends(get_db)
):
    db_user = await services.update_user(db, user_id, user_in)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


# 📌 Удалить пользователя по ID
@router.delete(
    "/{user_id}",
    summary="Delete user by ID",
    description="Delete specific user by their ID"
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await services.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"ok": True}


# 📌 Логин (вынес в отдельную группу)
@router.post(
    "/login", 
    response_model=schemas.Token, 
    tags=["Auth"],
    summary="User login",
    description="Authenticate user and get access token"
)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await auth.login(form_data, db)
