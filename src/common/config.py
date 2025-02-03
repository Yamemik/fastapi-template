from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # common
    app_name: str = "template"
    debug: bool = True
    # db
    string_connect="postgresql+asyncpg://postgres:postgres@localhost/postgres"

settings = Settings()
