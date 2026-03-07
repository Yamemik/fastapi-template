from fastapi import APIRouter

from features.users.api.user_routes import UserRoutes, AuthRoutes


api_router = APIRouter(prefix="/api/v1")

# создаём экземпляры классов и подключаем их роутеры
api_router.include_router(AuthRoutes().router)
api_router.include_router(UserRoutes().router)