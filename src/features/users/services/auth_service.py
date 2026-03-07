# src/modules/users/auth_service.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status

from src.config.settings import settings
from src.common.security import verify_password
from ..models.user_repository import UserRepository
from ..models.user_models import User


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, login: str, password: str) -> User:
        user = await self.user_repo.get_by_login(login)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    def create_access_token(self, subject: str, expires_delta: timedelta | None = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        payload = {"exp": expire, "sub": str(subject)}
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
