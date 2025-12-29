from fastapi import HTTPException
from modules.auth.domain.entities import User as AuthUser


def check_admin(user: AuthUser):
    if "admin" not in getattr(user, "roles", []):
        raise HTTPException(status_code=403, detail="Admin privileges required")
