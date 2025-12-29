from modules.auth.domain.interfaces import AuthProvider


class MockAuthProvider(AuthProvider):
    async def authenticate(self, data):
        return {"user_id": 1}

    async def validate_token(self, token: str):
        return {"user_id": 1}
