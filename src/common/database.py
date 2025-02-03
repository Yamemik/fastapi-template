import os
from typing import AsyncGenerator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.config import settings


if settings.debug:
    SQLALCHEMY_DATABASE_URL = settings.string_connect
else:
    SQLALCHEMY_DATABASE_URL = os.getenv('STRING_CONNECT')

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)