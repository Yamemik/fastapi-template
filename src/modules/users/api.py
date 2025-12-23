from fastapi import APIRouter, Depends, HTTPException
from modules.auth.dependencies import get_current_user
from modules.auth.permissions import check_admin
from modules.users.application.dto import UserDTO
from modules.auth.domain.entities import User as AuthUser
from modules.users.application.use_cases import GetUserUseCase, ListUsersUseCase
from modules.users.dependencies import get_get_user_use_case, get_list_users_use_case


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserDTO])
async def list_users(
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
    skip: int = 0,
    limit: int = 100,
):
    return await use_case.execute(skip, limit)


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(
    user_id: int,
    current_user: AuthUser = Depends(get_current_user),  # auth
    use_case: GetUserUseCase = Depends(get_get_user_use_case),  # users
):
    # пример проверки роли / доступа
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user cannot access")
    
    # можно добавить проверку ролей: if "admin" not in current_user.roles: ...
    
    user_dto = await use_case.execute(user_id)
    if not user_dto:
        raise HTTPException(status_code=404, detail="User not found")
    return user_dto


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: AuthUser = Depends(get_current_user),
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    check_admin(current_user)
    # удаление пользователя через use-case / repo