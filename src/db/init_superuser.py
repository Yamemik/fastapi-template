from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.users.models import User
from src.config.settings import settings
from src.common.security import get_password_hash


async def create_superuser_if_not_exists(db: AsyncSession):
    result = await db.execute(
        select(User).where(User.username == settings.SUPERUSER_NAME)
    )
    superuser = result.scalar_one_or_none()

    if superuser is None:
        superuser = User(
            username=settings.SUPERUSER_NAME,
            email=settings.SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
            is_superuser=True,
            is_active=True
        )
        db.add(superuser)
        await db.commit()
        print(f"✅ Superuser '{settings.SUPERUSER_NAME}' created")
    else:
        print(f"ℹ Superuser '{settings.SUPERUSER_NAME}' already exists")
