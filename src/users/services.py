from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def get_user_by_id(db: AsyncSession, feedback_id: int) -> User | None:
    statement = select(User).where(User.id == feedback_id)
    selected_feedback = await db.execute(statement)
    return selected_feedback.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> ScalarResult | None:
    limit = limit if limit > 10 else 10
    statement = select(User).offset(skip).limit(limit)
    selected_feedbacks = await db.execute(statement)
    return selected_feedbacks.scalars()