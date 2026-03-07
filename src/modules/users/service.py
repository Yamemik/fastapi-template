# src/modules/users/service.py

from src.config.settings import settings
from src.common.security import get_password_hash
from .repository import UserRepository
from .models import User
from .schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def get_user_by_login(self, login: str) -> User | None:
        return await self.repo.get_by_login(login)

    async def get_users(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip, limit)

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)

        user = User(
            login=user_data.login,
            email=user_data.email,
            hashed_password=hashed_password,
            surname=user_data.surname,
            name=user_data.name,
            patr=user_data.patr,
            is_admin=user_data.is_admin,
        )

        await self.repo.add(user)
        await self.repo.db.commit()
        await self.repo.db.refresh(user)

        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        db_user = await self.repo.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user_data.dict(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.repo.db.commit()
        await self.repo.db.refresh(db_user)

        return db_user

    async def delete_user(self, user_id: int) -> bool:
        db_user = await self.repo.get_by_id(user_id)
        if not db_user:
            return False

        await self.repo.delete(db_user)
        await self.repo.db.commit()
        return True

    async def create_superuser_if_not_exists(self) -> User:
        user = await self.repo.get_by_login(settings.SUPERUSER_NAME)

        if user:
            return user

        superuser = User(
            login=settings.SUPERUSER_NAME,
            email=settings.SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD or ""),
            surname="Admin",
            name="Admin",
            is_admin=True,
        )

        await self.repo.add(superuser)
        await self.repo.db.commit()
        await self.repo.db.refresh(superuser)

        return superuser
