from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Literal


class JWTManager:
    """
    Менеджер для работы с JWT-токенами.
    Поддерживает access и refresh токены с проверкой типа.
    """

    def __init__(
        self,
        secret: str,
        algorithm: str,
        access_expire_minutes: int,
        refresh_expire_days: int,
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.access_expire = timedelta(minutes=access_expire_minutes)
        self.refresh_expire = timedelta(days=refresh_expire_days)


    def _create_token(self, user_id: int, token_type: Literal["access", "refresh"]) -> str:
        now = datetime.now(timezone.utc)
        expire_delta = self.access_expire if token_type == "access" else self.refresh_expire

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + expire_delta,
            "type": token_type,
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)


    def create_access_token(self, user_id: int) -> str:
        return self._create_token(user_id, token_type="access")


    def create_refresh_token(self, user_id: int) -> str:
        return self._create_token(user_id, token_type="refresh")


    def decode(
        self,
        token: str,
        expected_type: Literal["access", "refresh"] | None = None,
    ) -> dict:
        """
        Декодирует JWT и проверяет тип токена (если указан).
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError("Invalid or expired token") from e

        token_type = payload.get("type")
        if expected_type and token_type != expected_type:
            raise ValueError(f"Unexpected token type: expected '{expected_type}', got '{token_type}'")

        return payload
