from abc import ABC, abstractmethod
from .entities import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        ...
