from typing import AsyncGenerator
from src.db.session import AsyncSessionLocal


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
