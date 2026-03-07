from sqlalchemy.ext.asyncio import AsyncSession

from features.users.models.user_repository import UserRepository
from features.users.services.user_service import UserService


async def create_superuser_if_not_exists(db: AsyncSession):
    repo = UserRepository(db)
    service = UserService(repo)

    await service.create_superuser_if_not_exists()