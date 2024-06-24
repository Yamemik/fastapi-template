from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # common
    app_name: str = "template"
    debug: bool = True


settings = Settings()
