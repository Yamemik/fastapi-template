from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from src.common.dependencies import get_db
from src.modules.users.dependencies import get_current_user
from . import schemas, services
from . import schemas, services, auth


router = APIRouter()

@router.post("/", response_model=schemas.UserRead)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await services.register_user(user_in, db)

@router.post("/login", response_model=schemas.Token, tags=["Auth"])
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await auth.login(form_data, db)

@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user
