from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.users.domain.entities import User
from modules.users.domain.repositories import UserRepository
from .models import UserModel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return User(
            id=model.id,
            email=model.email,
            is_active=model.is_active,
            full_name=model.full_name
        )

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        return [
            User(
                id=m.id,
                email=m.email,
                is_active=m.is_active,
                full_name=m.full_name
            )
            for m in result.scalars().all()
        ]
