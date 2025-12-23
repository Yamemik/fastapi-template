from pydantic import BaseModel


class LoginCommand(BaseModel):
    email: str
    password: str


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
