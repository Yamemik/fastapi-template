from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt

from src.common.security import get_password_hash
from . import models, schemas


async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    hashed_password = bcrypt.hash(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_superuser(db: AsyncSession, email: str, password: str) -> models.User:
    hashed_password = get_password_hash(password)
    user = models.User(
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()
