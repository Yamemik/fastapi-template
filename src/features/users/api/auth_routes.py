from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.user_schema import UserCreate, UserWithToken, Token
from ..dependencies import get_auth_service, get_user_service
from ..services.auth_service import AuthService
from ..services.user_service import UserService


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
        async def register(
            user_in: UserCreate,
            service: UserService = Depends(get_user_service),
            auth_service: AuthService = Depends(get_auth_service)
        ):
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
