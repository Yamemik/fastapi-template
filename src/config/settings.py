from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    DEBUG: bool = True
    
    # db
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    
    # superuser
    SUPERUSER_NAME: str = "admin"
    SUPERUSER_EMAIL: str = "kuancarlos@mail.ru"
    SUPERUSER_PASSWORD: str
    
    # jwt    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
