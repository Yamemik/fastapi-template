# src/users/routes.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.users.auth_service import AuthService

from .schemas import (
    UserCreate,
    UserUpdate,
    UserOut,
    UserOutWithoutToken,
    UserWithToken,
    Token,
)
from .models import User
from .dependencies import get_auth_service, get_current_user, get_user_service
from .service import UserService


class AuthRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Auth"])
        self._register_routes()

    def _register_routes(self):
        @self.router.post(
            "/register",
            response_model=UserWithToken,
            status_code=status.HTTP_201_CREATED,
        )
        async def register(user_in: UserCreate,
                           service: UserService = Depends(get_user_service),
                           auth_service: AuthService = Depends(get_auth_service)):
            existing = await service.get_user_by_login(user_in.login)
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")

            user = await service.create_user(user_in)
            access_token = auth_service.create_access_token(subject=str(user.id))

            return UserWithToken(
                id=user.id,
                login=user.login,
                surname=user.surname,
                name=user.name,
                patr=user.patr,
                is_admin=user.is_admin,
                created_at=user.created_at,
                access_token=access_token,
            )

        @self.router.post("/login", response_model=Token)
        async def login(
            form_data: OAuth2PasswordRequestForm = Depends(),
            auth_service: AuthService = Depends(get_auth_service)
        ):
            user = await auth_service.authenticate_user(form_data.username, form_data.password)
            token = auth_service.create_access_token(subject=str(user.id))
            return Token(access_token=token, token_type="bearer")


class UserRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=list[UserOut])
        async def read_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
            return await service.get_users(skip, limit)

        @self.router.get("/{user_id}", response_model=UserOut)
        async def read_user(user_id: int, service: UserService = Depends(get_user_service)):
            user = await service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        @self.router.get("/me", response_model=UserOutWithoutToken)
        async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
            return current_user

        @self.router.put("/me", response_model=UserOut)
        async def update_current_user(user_in: UserUpdate,
                                      current_user: Annotated[User, Depends(get_current_user)],
                                      service: UserService = Depends(get_user_service)):
            return await service.update_user(current_user.id, user_in)

        @self.router.delete("/{user_id}")
        async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
            success = await service.delete_user(user_id)
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            return {"ok": True}
