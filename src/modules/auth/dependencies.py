from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from modules.auth.infrastructure.security import decode_token
from modules.auth.infrastructure.repository import SqlAlchemyUserRepository
from modules.auth.application.use_cases import GetCurrentUserUseCase, LoginUseCase
from modules.auth.domain.entities import User


def get_login_use_case(
    session: AsyncSession = Depends(get_session),
) -> LoginUseCase:
    repo = SqlAlchemyUserRepository(session)
    return LoginUseCase(repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        user_id = decode_token(token)
        repo = SqlAlchemyUserRepository(session)
        use_case = GetCurrentUserUseCase(repo)
        return await use_case.execute(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    if token is None:
        return None  # нет токена → анонимный пользователь

    try:
        user_id = decode_token(token)
        repo = SqlAlchemyUserRepository(session)
        use_case = GetCurrentUserUseCase(repo)
        return await use_case.execute(user_id)
    except Exception:
        return None  # некорректный токен → анонимный