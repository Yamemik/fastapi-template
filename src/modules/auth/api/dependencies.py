from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# config / settings
from config.dependencies import get_settings

# users
from modules.auth.application.refresh_service import RefreshService
from modules.users.dependencies import get_user_repository

# auth
from modules.auth.application.auth_service import AuthService
from modules.auth.domain.types.auth_type import AuthType
from modules.auth.domain.exceptions import InvalidToken
from modules.auth.infrastructure.registry import get_auth_provider
from modules.auth.infrastructure.utils.jwt_manager import JWTManager
from modules.auth.infrastructure.utils.password import PasswordHasher


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_jwt_manager(settings=Depends(get_settings)) -> JWTManager:
    return JWTManager(
        secret=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_auth_service(
    settings=Depends(get_settings),
    user_repo=Depends(get_user_repository),
    jwt=Depends(get_jwt_manager),
    hasher=Depends(get_password_hasher),
):
    ProviderCls = get_auth_provider(AuthType(settings.AUTH_PROVIDER))
    provider = ProviderCls(jwt_manager=jwt, password_hasher=hasher)
    return AuthService(user_repo, provider)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_provider = get_auth_provider()
    try:
        user_data = await auth_provider.validate_token(token)
        return user_data
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
        
        
def get_refresh_service(
    settings=Depends(get_settings),
    user_repo=Depends(get_user_repository),
    jwt=Depends(get_jwt_manager),
):
    return RefreshService(jwt_manager=jwt, refresh_repo=..., user_repo=user_repo)