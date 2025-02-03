from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_async_session
import schemas
import services


router = APIRouter(
    prefix="/api/users",
    tags=["Пользователи"],
)


def get_db():
    db = get_async_session()
    try:
        yield db
    finally:
        db.aclose()
        

@router.get(
    "",
    response_model=list[schemas.UserReadSchema],
    summary="Получить пользователей",
    status_code=status.HTTP_202_ACCEPTED
)
def read_users(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    selected_feedbacks = services.get_users(db, skip=skip, limit=limit)
    return selected_feedbacks
