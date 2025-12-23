from fastapi import APIRouter, Depends
from modules.auth.application.dto import LoginCommand, TokenDTO
from modules.auth.application.use_cases import LoginUseCase
from modules.auth.dependencies import get_login_use_case

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenDTO)
async def login(
    cmd: LoginCommand,
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    return await use_case.execute(cmd)
