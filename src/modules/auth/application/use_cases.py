from modules.auth.domain.repositories import UserRepository
from modules.auth.domain.entities import User
from modules.auth.infrastructure.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from .dto import LoginCommand, TokenDTO


class LoginUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, cmd: LoginCommand) -> TokenDTO:
        user = await self.user_repo.get_by_email(cmd.email)

        if not user or not verify_password(cmd.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return TokenDTO(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )


class GetCurrentUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        return user

