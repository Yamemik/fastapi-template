from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    email: str
    is_active: bool
    full_name: str | None = None
