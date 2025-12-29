from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])

class PasswordHasher:
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)
