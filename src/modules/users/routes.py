from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, services
from src.common.dependencies import get_db


router = APIRouter()

@router.post("/", response_model=schemas.UserRead)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await services.register_user(user_in, db)
