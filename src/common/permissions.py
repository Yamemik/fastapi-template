from fastapi import HTTPException
from features.users.models.user_models import User as AuthUser


def check_admin(user: AuthUser):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin privileges required")
