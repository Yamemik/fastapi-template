from modules.auth.domain.exceptions import InvalidCredentials, InvalidToken


class AuthService:
    def __init__(self, user_repo, auth_provider):
        self.user_repo = user_repo
        self.provider = auth_provider

    async def login(self, data):
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise InvalidCredentials()

        return await self.provider.authenticate(
            password=data.password,
            hashed_password=user.hashed_password,
            user_id=user.id,
        )

    async def get_current_user(self, token: str):
        identity = await self.provider.validate_token(token)

        user = await self.user_repo.get_by_id(identity.user_id)
        if not user:
            raise InvalidToken()

        return user
