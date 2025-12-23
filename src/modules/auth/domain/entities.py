from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    email: str
    hashed_password: str
    is_active: bool
