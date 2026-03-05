from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.login == login)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def add(self, user: User) -> None:
        self.db.add(user)

    async def delete(self, user: User) -> None:
        self.db.delete(user)
