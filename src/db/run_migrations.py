import asyncio
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext

from alembic import command
from sqlalchemy import create_engine
from src.config.settings import settings


def get_alembic_config() -> Config:
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)  # sync-URL!
    return cfg


def has_pending_migrations_sync() -> bool:
    cfg = get_alembic_config()
    script = ScriptDirectory.from_config(cfg)

    engine = create_engine(settings.DATABASE_URL_SYNC)  # обычный sync engine
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()

    head_rev = script.get_current_head()
    return current_rev != head_rev


async def run_migrations_if_needed():
    loop = asyncio.get_running_loop()
    if await loop.run_in_executor(None, has_pending_migrations_sync):
        print("🔄 Обнаружены новые миграции, выполняем upgrade...")
        await loop.run_in_executor(None, lambda: command.upgrade(get_alembic_config(), "head"))
        print("✅ Миграции успешно применены.")
    else:
        print("✅ Миграции не требуются — всё в актуальном состоянии.")
