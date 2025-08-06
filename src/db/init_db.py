from src.db.session import engine
from src.db.base import Base
from src.modules.users.models import User
import asyncio


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
