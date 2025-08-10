from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud


async def register_user(user_in: schemas.UserCreate, db: AsyncSession):
    return await crud.create_user(db, user_in)
