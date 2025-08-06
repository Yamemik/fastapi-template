import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from src.config.settings import settings
from src.db.base import Base
from src.modules.users.models import User  # Импортируй все модели вручную!


# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Получаем URL из settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Асинхронный движок
connectable = async_engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
    future=True,
)

async def run_migrations_online():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,  # Сравнение типов столбцов
    )
    with context.begin_transaction():
        context.run_migrations()

asyncio.run(run_migrations_online())
