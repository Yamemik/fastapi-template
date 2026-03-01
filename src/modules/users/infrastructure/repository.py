from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.auth.infrastructure.utils.password import PasswordHasher
from modules.users.domain.entities import User
from modules.users.domain.repositories import UserRepository
from .models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.password_hasher = PasswordHasher()

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

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)  # <- исправлено
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

    async def create_superuser(self, email: str, password: str, full_name: str = "Superuser") -> User:
        hashed_password = self.password_hasher.hash(password)
        # Создаём **модель БД**, а не доменный объект
        superuser_model = UserModel(
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True,
            full_name=full_name
        )
        self.session.add(superuser_model)
        await self.session.commit()
        await self.session.refresh(superuser_model)  # чтобы получить id
        # Возвращаем доменный User
        return User(
            id=superuser_model.id,
            email=superuser_model.email,
            is_active=superuser_model.is_active,
            full_name=superuser_model.full_name
        )
