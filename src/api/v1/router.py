from fastapi import APIRouter

from src.features.users.api.user_routes import UserRoutes
from src.features.users.api.auth_routes import AuthRoutes


api_router = APIRouter(prefix="/api/v1")

# создаём экземпляры классов и подключаем их роутеры
api_router.include_router(AuthRoutes().router)
api_router.include_router(UserRoutes().router)