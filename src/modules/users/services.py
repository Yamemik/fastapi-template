from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.settings import settings
from src.common.security import get_password_hash
from src.modules.users.models import User
from src.modules.users.schemas import UserCreate, UserUpdate


# Получить одного юзера по ID
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


# Получить юзера по email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# Получить список юзеров
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# Создать нового юзера
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        surname=user.surname,
        name=user.name,
        patr=user.patr,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Обновить данные юзера
async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User | None:
    db_user = await get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_data.dict(exclude_unset=True)

    # Обработка пароля
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


# Удалить юзера
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


# Создать суперпользователя (если ещё не создан)
async def create_superuser_if_not_exists(db: AsyncSession):
    result = await db.execute(select(User).where(User.email == settings.SUPERUSER_EMAIL))
    superuser = result.scalar_one_or_none()

    if superuser is None:
        superuser = User(
            email=settings.SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
            surname="Admin",
            name="Admin",
            is_admin=True,
        )
        db.add(superuser)
        await db.commit()
        print(f"✅ Superuser '{settings.SUPERUSER_EMAIL}' created")
    else:
        print(f"ℹ Superuser '{settings.SUPERUSER_EMAIL}' already exists")
