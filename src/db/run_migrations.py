import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.config.settings import settings
from src.db.base import Base
from src.modules.users.models import User  # Импортируй все модели

from alembic.config import Config


async def run_async_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    connectable = async_engine_from_config(
        alembic_cfg.get_section(alembic_cfg.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
            render_as_batch=True  # для SQLite
        )

        async with context.begin_transaction():
            context.run_migrations()

    await connectable.dispose()


def run_migrations():
    asyncio.run(run_async_migrations())
