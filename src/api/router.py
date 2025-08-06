from fastapi import APIRouter
from src.modules.users.routes import router as users_router
from src.modules.items.routes import router as items_router  # если есть


api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(items_router, prefix="/items", tags=["Items"])
