from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

from src.config.settings import settings
from src.modules.users.services import get_user_by_email
from src.common.security import verify_password
from src.common.dependencies import get_db
from src.modules.users.schemas import Token
from src.modules.users.models import User


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"exp": expire, "sub": subject}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    # Добавляем логирование для отладки
    logger.info(f"Login attempt for username: {form_data.username}")
    
    user = await get_user_by_email(db, form_data.username)
    logger.info(f"User found: {user}")

    if not user:
        logger.warning(f"User not found for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Проверяем пароль с логированием
    logger.info(f"Verifying password for user: {user.email}")
    password_valid = verify_password(form_data.password, user.hashed_password)
    logger.info(f"Password verification result: {password_valid}")
    
    if not password_valid:
        logger.warning(f"Invalid password for user: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Создаем токен
    access_token = create_access_token(subject=str(user.id))
    logger.info(f"Access token created for user: {user.id}")
    
    return Token(access_token=access_token, token_type="bearer")