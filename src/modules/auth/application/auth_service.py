from src.modules.auth.domain.exceptions import InvalidCredentials, InvalidToken
from src.modules.auth.infrastructure.providers.local_jwt import LocalJWTAuthProvider
from ..api.schemas import LoginRequest 


class AuthService:
    def __init__(self, user_repo, auth_provider):
        self.user_repo = user_repo
        self.provider = auth_provider


    async def login(self, data: LoginRequest) -> dict:
        """
        data: LoginRequest(email, password)
        """
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise InvalidCredentials("Invalid email or password")

        # провайдер через интерфейс
        return await self.provider.authenticate(data)


    async def get_current_user(self, token: str):
        """
        Возвращает объект пользователя по токену
        """
        identity = await self.provider.validate_token(token)
        user_id = identity["id"]

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidToken("User not found")

        return user
