import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.db.session import engine, AsyncSessionLocal
from src.db.base import Base
from src.db.init_superuser import create_superuser_if_not_exists
from src.db.run_migrations import run_migrations_if_needed
from src.config.settings import settings


async def init_db():
    """Инициализация БД:
    - При первом запуске (без Alembic) → create_all
    - При наличии Alembic → проверка и выполнение миграций (если разрешено)
    - Создание суперюзера
    """

    alembic_present = False

    # Проверка наличия alembic_version
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT to_regclass('public.alembic_version')"))
        alembic_present = bool(result.scalar())

        if not alembic_present:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Таблицы созданы через create_all (первый запуск).")

    # Выполняем миграции, если Alembic есть и миграции разрешены
    if alembic_present and settings.USE_MIGRATIONS:
        await run_migrations_if_needed()
    elif alembic_present:
        print("ℹ Alembic найден, но миграции отключены (USE_MIGRATIONS=False).")

    # Создаём суперюзера
    async with AsyncSessionLocal() as session:
        await create_superuser_if_not_exists(session)
