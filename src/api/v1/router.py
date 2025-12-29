from fastapi import APIRouter
from modules.auth.api.router import router as auth_router
from modules.users.api import router as users_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router, prefix="/users", tags=["Users"])
