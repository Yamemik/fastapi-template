from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import AsyncSessionLocal
from modules.users.infrastructure.repository import SqlAlchemyUserRepository
from modules.users.application.use_cases import GetUserUseCase, ListUsersUseCase


def get_user_repository(session: AsyncSession = Depends(AsyncSessionLocal)):
    return SqlAlchemyUserRepository(session)

def get_get_user_use_case(repo=Depends(get_user_repository)):
    return GetUserUseCase(repo)

def get_list_users_use_case(repo=Depends(get_user_repository)):
    return ListUsersUseCase(repo)
