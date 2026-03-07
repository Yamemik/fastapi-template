from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.user_schema import UserOut, UserOutWithoutToken, UserUpdate
from ..models.user_models import User
from ..dependencies import get_current_user, get_user_service
from ..services.user_service import UserService


class UserRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=List[UserOut])
        async def read_users(
            skip: int = 0,
            limit: int = 100,
            service: UserService = Depends(get_user_service)
        ):
            return await service.get_users(skip, limit)

        @self.router.get("/{user_id}", response_model=UserOut)
        async def read_user(
            user_id: int,
            service: UserService = Depends(get_user_service)
        ):
            user = await service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        @self.router.get("/me", response_model=UserOutWithoutToken)
        async def read_current_user(
            current_user: Annotated[User, Depends(get_current_user)]
        ):
            return current_user

        @self.router.put("/me", response_model=UserOut)
        async def update_current_user(
            user_in: UserUpdate,
            current_user: Annotated[User, Depends(get_current_user)],
            service: UserService = Depends(get_user_service)
        ):
            return await service.update_user(current_user.id, user_in)

        @self.router.delete("/{user_id}")
        async def delete_user(
            user_id: int,
            service: UserService = Depends(get_user_service)
        ):
            success = await service.delete_user(user_id)
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            return {"ok": True}
