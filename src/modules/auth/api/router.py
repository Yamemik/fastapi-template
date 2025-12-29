from fastapi import APIRouter, Depends

from modules.auth.api.dependencies import get_auth_service, get_refresh_service
from modules.auth.api.schemas import LoginRequest, TokenRefreshRequest
from modules.auth.application.auth_service import AuthService
from modules.auth.application.refresh_service import RefreshService
from modules.auth.api.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(data)

@router.post("/refresh")
async def refresh(
    data: TokenRefreshRequest,
    service: RefreshService = Depends(get_refresh_service)
):
    return await service.refresh(data.refresh_token)

@router.post("/logout")
async def logout(
    data: TokenRefreshRequest,
    service: RefreshService = Depends(get_refresh_service)
):
    await service.logout(data.refresh_token)
    return {"detail": "Logged out"}

@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user
