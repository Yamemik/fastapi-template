from abc import ABC, abstractmethod


class AuthProvider(ABC):
    @abstractmethod
    async def authenticate(self, data) -> dict:
        """Логин / аутентификация"""

    @abstractmethod
    async def validate_token(self, token: str) -> dict:
        """Получение текущего пользователя"""
