from datetime import datetime
from enum import Enum

from pydantic import ConfigDict, BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    UNKNOWN = "unknown"


class UserReadSchema(BaseModel):
    id: int = Field(...)
    created_at: datetime = Field(...)
    email: EmailStr
    surname = Field(min_length=1, max_length=128)
    name = Field(min_length=1, max_length=128)
    patr = Field(max_length=128)
    is_admin: bool = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "text": "Супер уроки!",
                "rate": 5,
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        },
    )