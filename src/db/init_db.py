from src.db.session import engine, AsyncSessionLocal
from src.db.base import Base
from src.db.init_superuser import create_superuser_if_not_exists


async def init_db():
    # создание таблиц, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # создание суперюзера, если его нет
    async with AsyncSessionLocal() as session:
        await create_superuser_if_not_exists(session)
