from sqlalchemy.ext.asyncio import AsyncSession
from src.config.settings import settings
from src.modules.users.infrastructure.repository import SqlAlchemyUserRepository


async def create_superuser_if_not_exists(db: AsyncSession):
    user_repo = SqlAlchemyUserRepository(db)
    existing = await user_repo.get_by_email(settings.SUPERUSER_EMAIL)

    if existing is None:
        await user_repo.create_superuser(
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD
        )
        print(f"✅ Superuser '{settings.SUPERUSER_EMAIL}' created")
    else:
        print(f"ℹ Superuser '{settings.SUPERUSER_EMAIL}' already exists")
