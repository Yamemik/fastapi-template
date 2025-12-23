from modules.users.domain.repositories import UserRepository
from .dto import UserDTO

class GetUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int) -> UserDTO | None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        return UserDTO(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            full_name=user.full_name
        )

class ListUsersUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        users = await self.repo.list_users(skip, limit)
        return [
            UserDTO(
                id=u.id,
                email=u.email,
                is_active=u.is_active,
                full_name=u.full_name
            ) for u in users
        ]
