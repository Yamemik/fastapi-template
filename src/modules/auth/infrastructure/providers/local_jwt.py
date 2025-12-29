from modules.auth.domain.interfaces import AuthProvider
from modules.auth.domain.models import AuthIdentity
from modules.auth.domain.exceptions import InvalidCredentials, InvalidToken


class LocalJWTAuthProvider(AuthProvider):
    def __init__(self, jwt_manager, password_hasher):
        self.jwt = jwt_manager
        self.hasher = password_hasher


    async def authenticate(self, password, hashed_password, user_id) -> dict:
        if not self.hasher.verify(password, hashed_password):
            raise InvalidCredentials()


        return {
            "access_token": self.jwt.create_access_token(user_id),
            "refresh_token": self.jwt.create_refresh_token(user_id),
            "token_type": "bearer",
        }


    async def validate_token(self, token: str) -> AuthIdentity:
        try:
            payload = self.jwt.decode(token)
            user_id = int(payload["sub"])
        except Exception:
            raise InvalidToken()

        return AuthIdentity(user_id=user_id)
