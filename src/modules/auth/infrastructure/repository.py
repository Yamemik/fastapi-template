from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.auth.domain.entities import User
from modules.auth.domain.repositories import UserRepository
from .models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
        )
