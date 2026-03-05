from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService


async def create_superuser_if_not_exists(db: AsyncSession):
    repo = UserRepository(db)
    service = UserService(repo)

    await service.create_superuser_if_not_exists()