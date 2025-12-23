from abc import ABC, abstractmethod
from .entities import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        ...
