from fastapi import Depends
from functools import lru_cache

from config.settings import Settings


@lru_cache() 
def get_settings() -> Settings:
    """
    Возвращает объект настроек.
    Кэшируется для производительности.
    """
    return Settings()
