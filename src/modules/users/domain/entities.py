from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: int
    email: str
    is_active: bool
    full_name: str | None = None
