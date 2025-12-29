from pydantic_settings import BaseSettings, SettingsConfigDict
from modules.auth.infrastructure.registry import AuthType


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True

    # auth
    AUTH_PROVIDER: AuthType = AuthType.LOCAL

    # database
    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    # superuser
    SUPERUSER_NAME: str = "admin"
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str | None = None

    # jwt
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
