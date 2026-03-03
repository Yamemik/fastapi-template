from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    login: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    login: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    patr: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int | None = None